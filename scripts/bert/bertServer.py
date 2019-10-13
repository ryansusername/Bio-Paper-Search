from bert_serving.server.helper import get_args_parser
from bert_serving.server import BertServer

args = get_args_parser().parse_args(['-model_dir', 'cased',
                                     '-port', '7010',
                                     '-port_out', '7011',
                                     '-max_seq_len', 'NONE',
                                     '-mask_cls_sep',
                                     '-num_worker', '1',
                                     '-cpu'])
server = BertServer(args)
server.start()
