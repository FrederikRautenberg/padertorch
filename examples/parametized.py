import pytorch_sanity as pts


class GRU(pts.parameterized.Parameterized):
    def __init__(self, nonlinearity='tanh'):
        pass


class LSTM(pts.parameterized.Parameterized):
    def __init__(self, peephole=False):
        pass


class DenseEncoder(pts.parameterized.Parameterized):
    def __init__(self, layers=2, nonlinearity='elu'):
        pass


class RecurrentEncoder(pts.parameterized.Parameterized):

    @classmethod
    def get_signature(self):
        defaults = super().get_signature()
        defaults['recurrent'] = {
            'cls': GRU,
        }
        return defaults

    def __init__(
            self,
            recurrent,
            layers=2,
            bidirectional=False,
    ):
        pass


class VAE(pts.parameterized.Parameterized):
    """
    >>> from pprint import pprint
    >>> pprint(VAE.get_config({}))
    {'cls': 'parametized.VAE',
     'kwargs': {'encoder': {'cls': 'parametized.DenseEncoder',
                            'kwargs': {'layers': 3, 'nonlinearity': 'sigmoid'}},
                'vae_param': 2}}
    >>> pprint(VAE.get_config({'encoder': {'cls': RecurrentEncoder}}))
    {'cls': 'parametized.VAE',
     'kwargs': {'encoder': {'cls': 'parametized.RecurrentEncoder',
                            'kwargs': {'bidirectional': False,
                                       'layers': 4,
                                       'recurrent': {'cls': 'parametized.GRU',
                                                     'kwargs': {'nonlinearity': 'tanh'}}}},
                'vae_param': 2}}
    """
    @classmethod
    def get_signature(self):
        defaults = super().get_signature()
        defaults['encoder'] = {
            'cls': DenseEncoder,
            'kwargs': {'layers': 5},
            DenseEncoder: {'layers': 3, 'nonlinearity': 'sigmoid'},
            RecurrentEncoder: {'layers': 4},
        }
        return defaults

    def __init__(self, encoder, vae_param=2):
        self.encoder = encoder
        self.vae_param = vae_param


import sacred
import sacred.run
import sacred.commands
exp = sacred.Experiment('vae')


@exp.config
def config():

    model = {}
    VAE.get_config(
        dict(
            encoder={
                'cls': RecurrentEncoder,
                RecurrentEncoder: dict(
                    recurrent={'cls': LSTM}
                ),
            },
        ),
        model,
    )


@exp.automain
def main(_config, _run: sacred.run.Run):
    """
    python parametized.py print_config
    python parametized.py print_config with model.kwargs.encoder.cls=RecurrentEncoder model.kwargs.vae_param=10
    """
    from IPython.lib.pretty import pprint
    sacred.commands.print_config(_run)

    model = VAE.from_config(_config['model'])

    print('Model config')
    pprint(model.config)
    print('Encoder config')
    pprint(model.encoder)