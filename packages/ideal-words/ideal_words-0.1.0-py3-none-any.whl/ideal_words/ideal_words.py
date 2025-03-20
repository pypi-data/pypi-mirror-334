from functools import reduce
from itertools import product
from math import isclose
from typing import Callable, Literal, Sequence

import torch
import torch.nn as nn
import torch.nn.functional as F
import tqdm
from torch.utils.data import DataLoader, TensorDataset


class FactorEmbedding:
    """
    Utility class that encapsulates the some additional logic needed to compute ideal words and scores. That is, how to
    compute text embeddings (e.g, a tokenizer and a text encoder), how to jointly represent a tuple (z_1, ..., z_k) as a
    string, and how to represent a single z_i as a string.

    By default, text is embedded using the given tokenizer and the forward method of the given text encoder, a tuple z
    is represented as a string by joining tuple elements with spaces, and a single zi is its own string representation.
    If you want to customize this behaviour, sub-type this class.
    """

    def __init__(
        self,
        txt_encoder: nn.Module,
        tokenizer: Callable[[list[str]], torch.Tensor],
        normalize: bool = True,
        batch_size: int = 64,
        device: str | None = None,
    ) -> None:
        """
        Parameters
        ----------
            txt_encoder: Text encoder for computing the text embeddings.

            tokenizer: Tokenizer object (or function) for converting text into a tensor.

            normalize: Optional boolean flag for controlling if the outputs of the text encoder should be normalized.
                Default: `True`.

            batch_size: Optional batch size parameter used for computing text embeddings. Default: `64`.

            device: Optional string for specifying which device to use for computing embeddings. If omitted, it will be
                set to `'cuda'` if available else to `'cpu'`. Default: `None`.
        """
        self.txt_encoder = txt_encoder
        self.tokenizer = tokenizer
        self.normalize = normalize
        self.batch_size = batch_size

        if device:
            self.device = device
        else:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    @torch.no_grad()
    def embedding_fn(self, text: list[str], disable_pbar: bool = False) -> torch.Tensor:
        """
        Generic method for computing text embeddings given a tokenizer and a text encoder model. Internally, called by
        the `IdealWords` class.

        Parameters
        ----------
            text: A list of string representations that will be tokenized and passed to the text encoder.

            disable_pbar: Optional boolean flag for disabling the tqdm progress bar.
        """
        self.txt_encoder.eval()
        self.txt_encoder.to(self.device)

        prompts = self.tokenizer(text)
        embeddings = []
        for batch in tqdm.tqdm(
            DataLoader(TensorDataset(prompts), batch_size=self.batch_size, shuffle=False),
            desc='Compute embeddings',
            disable=disable_pbar,
        ):
            embeddings.append(self.encode_text(batch[0].to(self.device)))
        embeddings = torch.cat(embeddings)

        return F.normalize(embeddings) if self.normalize else embeddings

    def encode_text(self, text: torch.Tensor) -> torch.Tensor:
        """
        Method that specifies how the text encoder should be used to compute embeddings. Overwrite this method if you
        don't want to use the forward method of your encoder to embed text.

        Parameters
        ----------
            text: Tensor containing the tokenized text representations of shape (batch_size, context_length)
        """
        return self.txt_encoder(text)

    def joint_repr(self, z: tuple[str, ...]) -> str:
        """
        Method that specifies how a tuple z in Z_1 x ... x Z_k should be represented as text. For example, the tuple
        `('blue', 'car')` might be represented as `'an image of a blue car'`. Overwrite this method if you don't want to
        simply join the tuple using spaces.

        Parameters
        ----------
            z: A tuple containing strings (one per factor) to be represented as a single string.
        """
        return ' '.join(z)

    def single_repr(self, zi: str, factor_idx: int) -> str:
        """
        Method that specifies how an element zi in Z_j should be represented as text. For example, the element
        `'blue'` might be represented as `'an image of a blue object'`. Overwrite this method if you don't want to
        simply use the element itself as a representation.

        Parameters
        ----------
            zi: A string representing an element of a specified factor Z_j.

            factor_idx: Zero-based index of the factor Z_j to which zi belongs.
        """
        _ = factor_idx
        return zi


class IdealWords:
    """
    Class for computing ideal word representations for a given factor embedding and factors. Optionally, weights for the
    individual elements of the factors can be specified.
    """

    def __init__(
        self,
        factor_embedding: FactorEmbedding,
        factors: list[list[str]],
        weights: list[list[float]] | None = None,
        score_mode: Literal['avg_dist', 'avg_sq_dist', 'paper_repro'] = 'avg_sq_dist',
        verbose: int = 1,
    ) -> None:
        """
        Parameters
        ----------
            factor_embedding: Factor embedding that handles text embedding and single/joint representation logic.

            factors: List of lists of strings where each list represents the elements of a factor.

            weights: Optional list of lists of floats where each list represents the weights for the elements of the
                factors. If omitted, uniform weights for all factor elements will be used. Default: `None`.

            score_mode: Optional flag to customize score computation.
                'avg_dist' - uses the average euclidean between embedding vectors for iw, rw, and avg score
                'avg_sq_dist' - uses the average squared euclidean between embedding vectors for iw, rw, and avg score
                'paper_repro' - uses average euclidean distance for iw and rw score and average squared euclidean
                    distance for avg score, empirically this seems to be what they used in their paper (Tables 6 and 7)
                In the paper, they state that they use squared distance everywhere which is why we choose this mode as
                the default. However, to reproduce the results from the paper, use the 'paper_repro' mode (for details
                see https://github.com/icetube23/ideal_words/issues/1). Default: `'avg_sq_dist'`.

            verbose: Optional int parameter to customize verbosity level.
                0 - show no tqdm progress bar at all
                1 - show tqdm progress bar during ideal word computation
                2 - show tqdm progress bar during ideal and real word computation
                Default: `1`.
        """
        # verify factors are disjoint
        assert len(reduce(lambda u, v: u | v, [set(factor) for factor in factors])) == sum(
            [len(factor) for factor in factors]
        ), 'Factors are expected to be disjoint.'

        self.factor_embedding = factor_embedding
        self.factors = factors
        self.pairs = list(product(*self.factors))
        self.pair2idx = {pair: i for i, pair in enumerate(self.pairs)}
        self.factor2idx = {zi: (i, j) for i, factor in enumerate(self.factors) for j, zi in enumerate(factor)}
        self.weights = weights if weights else [[1 / len(factor)] * len(factor) for factor in factors]
        self.device = self.factor_embedding.device

        assert score_mode in ['avg_dist', 'avg_sq_dist', 'paper_repro'], f'Invalid score mode: {score_mode}'
        self.score_mode = score_mode
        assert verbose in [0, 1, 2]
        self.verbose = verbose

        # verify weights
        assert len(self.factors) == len(self.weights)
        for factor, weight in zip(self.factors, self.weights):
            assert len(factor) == len(weight)
            assert isclose(sum(weight), 1)

        # precompute indices over which we need to average later
        self.factor_indices = [{zi: [] for zi in factor} for factor in self.factors]
        for i, z in enumerate(self.pairs):
            for j, zi in enumerate(z):
                self.factor_indices[j][zi].append(i)

        # compute embeddings and ideal words
        self._compute_ideal_words()

        # approximation cache
        self._uz: dict[str, torch.Tensor] = {}

        # lazily computed real words
        self.real_words = None

        # lazily computed compositionality scores from the paper
        self._iw_score = None
        self._rw_score = None
        self._avg_score = None

        # lazily computed custom compositionality scores
        self._iw_accuracy = None
        self._rw_accuracy = None

    @torch.no_grad()
    def _compute_ideal_words(self) -> None:
        """Compute ideal words as in Equation 4 of the paper."""
        # expand factor / weight lists into paired representation to allow for tensor operations
        alphas = torch.tensor(list(product(*self.weights))).to(self.device).double()
        betas = alphas.prod(dim=1).unsqueeze(-1).double()

        # compute embeddings for each combination of factors
        captions = [self.factor_embedding.joint_repr(pair) for pair in self.pairs]
        embeddings = self.factor_embedding.embedding_fn(captions, disable_pbar=self.verbose < 1).double()

        # u_zero is a weighted average of all embeddings
        u_zero = (embeddings * betas).sum(dim=0)

        ideal_words = []
        for i, factor in enumerate(self.factors):
            # precompute weighted embeddings instead
            weighted_embeddings = alphas[:, i].reciprocal().unsqueeze(-1) * betas * embeddings

            # compute u_zi for each zi in factor Zi
            u_zi = []
            for zi in factor:
                inds = self.factor_indices[i][zi]
                u_zi.append(weighted_embeddings[inds].sum(dim=0))
            u_zi = torch.stack(u_zi) - u_zero
            ideal_words.append(u_zi.float())

        # we use double precision for the weighted averages but afterwards it is not really needed anymore
        self.embeddings = embeddings.float()
        self.u_zero = u_zero.float()
        self.ideal_words = ideal_words

    @torch.no_grad()
    def _compute_real_words(self) -> None:
        """Compute real words by encoding factor elements individually."""
        # real words are computed by embedding a prompt containing only info from a single factor at a time
        real_words = []
        for idx, factor in enumerate(self.factors):
            captions = [self.factor_embedding.single_repr(zi, idx) for zi in factor]
            embeddings = self.factor_embedding.embedding_fn(captions, disable_pbar=self.verbose < 2).float()
            real_words.append(embeddings)

        self.real_words = real_words

    @torch.no_grad()
    def _materialize_uz(self, approx: str) -> torch.Tensor:
        # if not already materialized and cached, compute approximations
        if approx not in self._uz:
            uz_hat = torch.stack([self.get_uz(pair, approx=approx) for pair in self.pairs])
            assert uz_hat.shape == self.embeddings.shape
            self._uz[approx] = uz_hat

        return self._uz[approx]

    def get_iw(self, zi: str) -> torch.Tensor:
        """Retrieve the ideal word representation of a given factor element."""
        assert zi in self.factor2idx, f'Unknown concept: {zi}'
        i, j = self.factor2idx[zi]
        return self.ideal_words[i][j]

    def get_rw(self, zi: str) -> torch.Tensor:
        """Retrieve the real word representation of a given factor element."""
        if self.real_words is None:
            self._compute_real_words()
            assert self.real_words is not None

        assert zi in self.factor2idx, f'Unknown concept: {zi}'
        i, j = self.factor2idx[zi]
        return self.real_words[i][j]

    def get_uz(self, z: Sequence[str], approx: str = 'ideal') -> torch.Tensor:
        """Compute an approximation to the actual embedding of tuple z using either ideal or real words."""
        assert len(z) == len(self.factors)

        # approximations are already cached and need not to be recomputed
        if approx in self._uz:
            idx = self.pair2idx[tuple(z)]
            return self._uz[approx][idx]

        if approx == 'ideal':
            return torch.stack([self.get_iw(zi) for zi in z]).sum(dim=0) + self.u_zero
        elif approx == 'real':
            return torch.stack([self.get_rw(zi) for zi in z]).mean(dim=0)
        else:
            raise ValueError(f'Invalid approximation mode: {approx}')

    def _score(self, approx: str) -> tuple[float, float]:
        # get word approximation for each combination of factors
        uz_hat = self._materialize_uz(approx)

        # compute distances between the compositional approximations and the actual embeddings
        dists = torch.linalg.vector_norm(self.embeddings - uz_hat, dim=1)

        # use average squared distance for score
        if self.score_mode == 'avg_sq_dist':
            dists.square_()

        return dists.mean().cpu().item(), dists.std().cpu().item()

    @property
    def iw_score(self) -> tuple[float, float]:
        """
        Retrieve the ideal words score, i.e., the average distance between the actual embeddings and the ideal word
        approximations. The first time this property is accessed the score will be computed and will be cached for
        successive accesses.
        """
        if self._iw_score is None:
            self._iw_score = self._score('ideal')

        return self._iw_score

    @property
    def rw_score(self) -> tuple[float, float]:
        """
        Retrieve the real words score, i.e., the average distance between the actual embeddings and the real word
        approximations. The first time this property is accessed the score will be computed and will be cached for
        successive accesses.
        """
        if self._rw_score is None:
            self._rw_score = self._score('real')

        return self._rw_score

    @property
    def avg_score(self) -> tuple[float, float]:
        """
        Compute the average pairwise distances between the actual embeddings. The first time this property is accessed
        the score will be computed and will be cached for successive accesses.
        """
        if self._avg_score is None:
            # compute pairwise distances of original embedding vectors
            embeddings = self.embeddings.half()  # save some memory as this metric is expensive to compute
            dists = torch.cdist(embeddings, embeddings, compute_mode='use_mm_for_euclid_dist')

            # dists is a symmetric matrix with diagonal 0 because cdist considers ordered pairs
            # so we only average over the upper triangular half of dists
            dists = dists[torch.ones_like(dists, dtype=torch.bool).triu(1)]

            # use average squared distance for score
            if self.score_mode == 'avg_sq_dist' or self.score_mode == 'paper_repro':
                dists.square_()

            self._avg_score = dists.mean().cpu().item(), dists.std().cpu().item()

        return self._avg_score

    def _accuracy(self, approx: str) -> float:
        # get word approximation for each combination of factors
        uz_hat = self._materialize_uz(approx).half()
        embeddings = self.embeddings.half()  # save some memory as this metric is expensive to comput

        # compute pairwise distances between the approximations and the actual embeddings
        dists = torch.cdist(embeddings, uz_hat, compute_mode='use_mm_for_euclid_dist')

        # find nearest neighbor for each approximated embedding and compare against expected nearest neighbors
        approx_matches = dists.argmin(dim=0)
        expected_matches = torch.arange(len(approx_matches), device=self.device)

        return (approx_matches == expected_matches).float().mean().cpu().item()

    @property
    def iw_accuracy(self) -> float:
        """
        Retrieve the ideal words accuracy, i.e., find the nearest actual embedding vector for each approximate embedding
        vector and compute the accuracy over how often the nearest neighbor matches the expected actual emebdding
        vector. The first time this property is accessed the score will be computed and will be cached for successive
        accesses.
        """
        if self._iw_accuracy is None:
            self._iw_accuracy = self._accuracy('ideal')

        return self._iw_accuracy

    @property
    def rw_accuracy(self) -> float:
        """
        Retrieve the real words accuracy, i.e., find the nearest actual embedding vector for each approximate embedding
        vector and compute the accuracy over how often the nearest neighbor matches the expected actual emebdding
        vector. The first time this property is accessed the score will be computed and will be cached for successive
        accesses.
        """
        if self._rw_accuracy is None:
            self._rw_accuracy = self._accuracy('real')

        return self._rw_accuracy
