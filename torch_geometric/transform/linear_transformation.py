import torch


class LinearTransformation(object):
    r"""Transforms all node positions with a square transformation matrix
    computed offline.

    Args:
        matrix (Tensor): tensor with shape :math:`[D x D]` where :math:`D`
            corresponds to the dimensionality of node positions.

    .. testsetup::

        import torch
        from torch_geometric.datasets.dataset import Data

    .. testcode::

        from torch_geometric.transform import LinearTransformation

        pos = torch.tensor([[-1, 1], [-3, 0], [2, -1]], dtype=torch.float)
        data = Data(None, pos, None, None, None)

        matrix = torch.tensor([[2, 0], [0, 2]], dtype=torch.float)
        data = LinearTransformation(matrix)(data)

        print(data.pos)

    .. testoutput::

        tensor([[-2.,  2.],
                [-6.,  0.],
                [ 4., -2.]])
    """

    def __init__(self, matrix):
        assert matrix.dim() == 2, (
            'Transformation matrix should be two-dimensional.')
        assert matrix.size(0) == matrix.size(1), (
            'Transformation matrix should be square. Got [{} x {}] rectangular'
            'matrix.'.format(*matrix.size()))

        self.matrix = matrix

    def __call__(self, data):
        pos = data.pos.view(-1, 1) if data.pos.dim() == 1 else data.pos

        assert pos.size(1) == self.matrix.size(0), (
            'Node position and transformation matrix have incompatible shape.')

        data.pos = torch.mm(pos, self.matrix)

        return data

    def __repr__(self):
        matrix = str(self.matrix.cpu().numpy())[1:-1].split('\n')
        matrix = '\n'.join(['    {}'.format(row.strip()) for row in matrix])
        return '{}([\n{}\n])'.format(self.__class__.__name__, matrix)