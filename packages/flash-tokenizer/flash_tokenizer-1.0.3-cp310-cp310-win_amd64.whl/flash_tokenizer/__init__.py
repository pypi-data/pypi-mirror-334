from ._core import FlashBertTokenizer, FlashBertTokenizerBidirectional
from .batch_encoding import BatchEncoding
import numpy as np


class BertTokenizerFlash:

    def __init__(self, vocab_file, do_lower_case=True,
                 unk_token="[UNK]",
                 sep_token="[SEP]",
                 pad_token="[PAD]",
                 cls_token="[CLS]",
                 mask_token="[MASK]",
                 tokenize_chinese_chars=True,
                 strip_accents=None,
                 clean_up_tokenization_spaces=True,
                 suffix_indicator="##",
                 bidirectional=False,
                 **kwargs):
        if bidirectional:
            self.tokenizer = FlashBertTokenizerBidirectional(vocab_file, do_lower_case)
        else:
            self.tokenizer = FlashBertTokenizer(vocab_file, do_lower_case)
        self.__version = self.tokenizer.version()
        pass

    @property
    def version(self):
        return self.__version;

    def __call__(self,
                 text: str | list[str] | None = None,
                 text_pair: str | list[str] | None = None,
                 text_target: str | list[str] | None = None,
                 text_pair_target: str | list[str] | None = None,
                 add_special_tokens: bool = True,
                 padding: bool | str = False,
                 truncation: bool | str | None = None,
                 max_length: int | None = None,
                 stride: int = 0,
                 is_split_into_words: bool = False,
                 pad_to_multiple_of: int | None = None,
                 padding_side: bool | None = None,
                 return_tensors: str | None = None,
                 return_token_type_ids: bool = True,
                 return_attention_mask: bool = True,
                 return_overflowing_tokens: bool = False,
                 return_special_tokens_mask: bool = False,
                 return_offsets_mapping: bool = False,
                 return_length: bool = False,
                 verbose: bool = True,
                 suffix_indicator: str = '##'):
        if isinstance(text, str):
            input_ids = [self.tokenizer.encode(text, padding, max_length)]
        elif isinstance(text, list):
            input_ids = self.tokenizer.batch_encode(text, padding, max_length)
        else:
            raise ValueError("text must be str or list[str].")
        if return_tensors == "np":
            input_ids = np.asarray(input_ids)
        return BatchEncoding(input_ids, return_attention_mask=return_attention_mask,
                             return_token_type_ids=return_token_type_ids)


# __all__ = ["FlashBertTokenizer", "FlashBertTokenizerBidirectional", "BertTokenizerFlash"]
__all__ = ["BertTokenizerFlash", "BatchEncoding"]
