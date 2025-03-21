import benpy.draw


def draw3d(sol_mofba, which="Primal", **kargs):
    """ Returns a 3D figure of the Pareto Front. """
    pol=None
    if which=="Primal":
        pol=sol_mofba.Primal
    elif which=="Dual":
        pol=sol_mofba.Dual
    return benpy.draw.draw3d(pol, **kargs)


def draw2d(sol_mofba,which="Primal", **kargs):
    """Return a 2D figure of the pareto Front. """
    pol=None
    if which=="Primal":
        pol=sol_mofba.Primal
    elif which=="Dual":
        pol=sol_mofba.Dual
    return benpy.draw.draw2d(pol,**kargs)


def drawNd(sol_mofba,which="Primal", **kargs):
    """Return a radial plot of the Pareto Front."""
    pol=None
    if which=="Primal":
        pol=sol_mofba.Primal
    elif which=="Dual":
        pol=sol_mofba.Dual
    return benpy.draw.drawNd(pol, **kargs)
