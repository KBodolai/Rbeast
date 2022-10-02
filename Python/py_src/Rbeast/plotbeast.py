import matplotlib.pyplot as plt
import numpy             as np
from   .extractbeast     import extract as extractbeast

import warnings

VARS    = ['st', 's', 't', 'scp', 'tcp', 'sorder', 'torder', 'error', 'o', 'ocp', 'samp', 'tslp', 'slpsgn']
YLABELS = {'st': 'Y', 's': 'season', 't': 'trend', 'o': 'outlier', 'scp': 'Pr(scp)', 'tcp': 'Pr(tcp)', 'ocp': 'Pr(ocp)',
           'sorder': 'sOrder', 'torder': 'tOrder', 'samp': 'amplitude', 'tslp': 'tslp', 'slpsgn': 'slpsgn',
           'error': 'error'}
COLORS  = {'st': [0.1, 0.1, 0.1], 's': 'r', 't': 'g', 'o': 'b', 'scp': 'r', 'tcp': 'g', 'ocp': 'b', 'sorder': 'r',
        'torder': 'g', 'samp': 'r', 'tslp': 'g', 'slpsgn': 'k', 'error': [0.4, 0.4, 0.4]}
HEIGHTS = {'st': 0.8, 's': 0.8, 't': 0.8, 'o': 0.8, 'scp': .5, 'tcp': .5, 'ocp': .5, 'sorder': .5, 'torder': .5,
           'samp': .4, 'tslp': .4, 'slpsgn': .4, 'error': .4}

length  = len
isfield = hasattr
c       = np.concatenate
min     = np.min
max     = np.max


def getfield(obj, fld):
    if isinstance(obj, dict):
        return obj[fld]
    if hasattr(obj, '__dict__'):
        return obj.__dict__[fld]
    return None


def isempty(obj):
    if obj is None:
        return True
    if isinstance(obj, np.ndarray):
        return len(obj) == 0
    if hasattr(obj, '__dict__'):
        return len(obj.__dict__) == 0
    return len(obj) == 0


def plot(o, index=0,\
         vars       = ["st", "s", "scp", "sorder", "t", "tcp", "torder", "slpsgn", "o", "ocp", "error"], \
         ncpStat    = 'median', \
         relheights = [],\
         fig        = [], \
         title      = 'BEAST decompositon and changepoint detection',\
         ylabels    = [],\
         xlabel     = 'time'\
         ):
         
#    index = 0;
#    vars = ["st", "s", "scp", "sorder", "t", "tcp", "torder", "slpsgn", "o", "ocp", "error"]
#    relheights = []
#    ylabels = []
#    xlabel = 'time'

    class Obj:
        pass

    def error(msg):
        raise ValueError(msg)

    def warning(msg):
        warnings.warn(msg)

    #indexDefautValue    = 0;
    #varsDefautValue     = ["st", "s", "scp", "sorder", "t", "tcp", "torder", "slpsgn", "o", "ocp", "error"]
    #ncpStatDefaultValue = 'median'
    #vars    = varsDefautValue
    #ncpStat = ncpStatDefaultValue
    ncpStat = ncpStat.lower()
    vars    = [x.lower() for x in vars]
    varsold = vars.copy()
    vars    = [x for x in varsold if x in VARS]

    if  len(relheights) < len(varsold):
        heights = [HEIGHTS[key] for key in vars]
    else:
        heights = relheights[0:len(varsold)]
        heights = [heights[i] for i in range(len(varsold)) if varsold[i] in vars]

    if  len(ylabels) < len(varsold):
        ylab =  [YLABELS[key] for key in vars]
    else:
        ylab = ylabels[0:len(varsold)]
        ylab = [ylab[i] for i in range(len(varsold)) if varsold[i] in vars]
    # ylab    = {key:YLABLES[key] for key in vars}

    col     = [COLORS[key] for key in vars]


    if  length(o.marg_lik)> 1 :
        # more than time series is present
        o=extractbeast(o,index);        

    if np.isnan(o.marg_lik):
        H = [];
        warning("The result of the selected time series selected is invalid.");
        return None

    # %%
    hasData   = isfield(o, "data")   and  not isempty(getfield(o, 'data'));
    hasSeason = isfield(o, 'season') and not  isempty(o.season);
    if hasSeason:
        hasSOrder = isfield(o.season, 'order') and not  isempty(o.season.order);
        hasAmp    = isfield(o.season, 'amp')   and not isempty(o.season.amp);
    else:
        hasSOrder = False;
        hasAmp    = False;

    hasOutlier = isfield(o, 'outlier') and not isempty(o.outlier);
    hasTOrder  = isfield(o.trend, 'order') and not isempty(o.trend.order);
    hasSlp     = isfield(o.trend, 'slp') and not  isempty(o.trend.slp);

    has = Obj();
    has.hasAmp = hasAmp;
    has.hasSlp = hasSlp;
    has.hasSeason = hasSeason;
    has.hasSOrder = hasSOrder;
    has.hasTOrder = hasTOrder;
    has.hasOutlier = hasOutlier;
    has.hasData = hasData;

    # %%
    idx = [True for x in vars];
    if (not hasAmp):
        idx = [idx[i] if vars[i] != 'samp' else False for i in range(len(idx))]
    if (not hasSlp):
        idx = [idx[i] if vars[i] != 'tslp' and vars[i] !='slpsgn' else False for i in range(len(idx))]
    if (not hasSeason):
        idx = [idx[i] if vars[i] != 'st'     and vars[i] != 's' else False for i in range(len(idx))]
        idx = [idx[i] if vars[i] != 'sorder' and vars[i] != 'scp' else False for i in range(len(idx))]
    if (not hasSOrder):
        idx = [idx[i] if vars[i] != 'sorder' else False for i in range(len(idx))]
    if (not hasTOrder):
        idx = [idx[i] if vars[i] != 'torder' else False for i in range(len(idx))]
    if (not hasOutlier):
        idx = [idx[i] if vars[i] != 'o' and vars[i] != 'ocp' else False for i in range(len(idx))]
    if (not hasData):
        idx = [idx[i] if vars[i] != 'error' else False for i in range(len(idx))]

    vars  = [ vars[i] for i in range(len(idx)) if idx[i]]
    col   = [ col[i] for i in range(len(idx)) if idx[i]]
    ylab  = [ ylab[i] for i in range(len(idx)) if idx[i]]
    heights  = [ heights[i] for i in range(len(idx)) if idx[i]]

    nPlots = length(vars)
    if (nPlots == 0):
        error("No valid variable names speciffied int the 'vars' argument. Possible names include 'st','t','s','sorder','torder','scp','tcp','samp','tslp','o', 'ocp', and 'error'. ")


    #######################################################
    #  Functions and variables to load the outputs
    ########################################################

    opt = Obj()
    opt.leftmargin    = 0.1;
    opt.rightmargin   = 0.05;
    opt.topmargin     = 0.06;
    opt.bottommargin  = .08;
    opt.verticalspace = 0.01;

    if isempty(fig):
        fig = plt.figure()
    H=axeslayout(opt,heights, fig)

    #  #######################################################
    #  # Create a subplot given the relative heights of the vertical plots
    #  ########################################################
    x      = o
    t, N   = (x.time, length(x.time))
    t2t    = c( [t, np.flip(t)] )

    for i in range(len(vars)):
        ytitle, var, clr, h = ( ylab[i], vars[i], col[i], H[i])

        #cla(h); % cla
        if var == 'st' :
            Yts, YtsSD, Yerr = get_Yts(x, hasSeason, hasOutlier, hasData)
            plot_st(h, ytitle, has, clr, x, t, t2t, Yts, YtsSD)
        if (var == 's'):
            Y, SD, CI, Amp, AmpSD, Order = get_S(x, hasAmp, hasSOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_scp(x, ncpStat);
            plot_y(h, ytitle, has, clr, x, t, t2t, Y, CI, ncp, cp);
        if (var == 't'):
            Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order = get_T(x, hasSlp, hasTOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_tcp(x, ncpStat);
            plot_y(h, ytitle, has, clr, x, t, t2t, Y, CI, ncp, cp);
        if (var == 'scp'):
            Y, SD, CI, Amp, AmpSD, Order = get_S(x, hasAmp, hasSOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_scp(x, ncpStat);
            plot_prob(h, ytitle, has, clr, x, t, t2t, Prob1, Prob, ncp, cp);
        if (var == 'tcp'):
            Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order = get_T(x, hasSlp, hasTOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_tcp(x, ncpStat);
            plot_prob(h, ytitle, has, clr, x, t, t2t, Prob1, Prob, ncp, cp);
        if (var == 'sorder'):
            Y, SD, CI, Amp, AmpSD, Order = get_S(x, hasAmp, hasSOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_scp(x, ncpStat);
            plot_order(h, ytitle, has, clr, x, t, t2t, Order, ncp, cp);
        if (var == 'torder'):
            Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order = get_T(x, hasSlp, hasTOrder);
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_tcp(x, ncpStat);
            plot_order(h, ytitle, has, clr, x, t, t2t, Order, ncp, cp);
        if (var == 'samp'):
            Y, SD, CI, Amp, AmpSD, Order = get_S(x, hasAmp, hasSOrder);
            plot_amp(h, ytitle, has, clr, x, t, t2t, Amp, AmpSD);
        if (var == 'tslp'):
            Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order = get_T(x, hasSlp, hasTOrder);
            plot_slp(h, ytitle, has, clr, x, t, t2t, Slp, SlpSD)
        if (var == 'slpsgn'):
            Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order = get_T(x, hasSlp, hasTOrder);
            plot_slpsgn(h, ytitle, has, clr, x, t, t2t, SlpSignPos, SlpSignZero)
        if (var == 'o'):
            Y, SD, CI = get_O(x);
            plot_o(h, ytitle, has, clr, x, t, t2t, Y, SD);
        if (var == 'ocp'):
            cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1 = get_ocp(x, ncpStat);
            plot_oprob(h, ytitle, has, clr, x, t, t2t, Prob1, Prob, ncp, cp);
        if (var == 'error'):
            Yts, YtsSD, Yerr = get_Yts(x, hasSeason, hasOutlier, hasData);
            plot_error(h, ytitle, has, clr, x, t, t2t, Yerr);

        if i % 2 == 0:
            h.yaxis.tick_left()
        else:
            h.yaxis.tick_right()
        #https://stackoverflow.com/questions/63723514/userwarning-fixedformatter-should-only-be-used-together-with-fixedlocator
        #h.set_yticklabels(h.get_yticks(), rotation =90)
        h.tick_params(axis='y', labelrotation = 90)

        if (i == 0):
            fig.suptitle(title);

        if (i == nPlots-1):
            h.set_xlabel(xlabel);
        else:
            h.set_xlabel([]);

        h.set_ylabel(ytitle);
        h.yaxis.set_label_position('left')
        h.yaxis.set_label_coords(-0.08, 0.5)
        #h.yaxis.set_label_position('left')
        fig.show()
    #return {'fig':fig, 'ax':H}
    return fig, H


#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def axeslayout(opt, hLayout, fig):
    lm = opt.leftmargin;
    rm = opt.rightmargin;
    tm = opt.topmargin;
    bm = opt.bottommargin;
    vd = opt.verticalspace;
    # hLayout = [1 1 - 1 1 1 - 1 1 1];
    hLayout = np.array(hLayout)
    winList = np.where(hLayout > 0)[0]  # a tuple returned
    hgt = (1 - tm - bm - abs(np.sum(hLayout[hLayout < 0]) * vd)) / np.sum(hLayout[hLayout > 0]);
    H = [];
    fig.clf()
    ax = fig.subplots(len(winList), 1)  # plt.figure()  fig.add_axes
    for i in range(len(winList)):
        # H.append( fig.add_axes([0,i/4.0,1,1]) )
        idx = winList[i];
        if i == 0:
            yup = 1 - tm
        else:
            slist = hLayout[np.arange(1, len(hLayout) + 1) <= idx]
            slist[slist > 0] = slist[slist > 0] * hgt;
            slist[slist < 0] = -slist[slist < 0] * vd;
            yup = 1 - tm - sum(slist);
        #print([lm, yup - hLayout[idx] * hgt, 1 - rm - lm, hLayout[idx] * hgt])

        ax[i].set_position([lm, yup - hLayout[idx] * hgt, 1 - rm - lm, hLayout[idx] * hgt])

        # set(H(i), 'box', 'on');
    return ax

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def get_Yts(x, hasSeason, hasOutlier, hasData):
    Yts = x.trend.Y;
    SD2 = x.trend.SD ** 2 + x.sig2[0]
    if hasSeason:
        Yts, SD2 = (Yts + x.season.Y, SD2 + x.season.SD ** 2)
    if hasOutlier:
        Yts, SD2 = (Yts + x.outlier.Y, SD2 + x.outlier.SD ** 2)
    SD    = np.sqrt(SD2)
    tmp   = Yts + SD
    YtsSD = np.concatenate([Yts - SD, np.flip(tmp)])
    if hasData:
        Yerr = x.data - Yts
    else:
        Yerr = [];
    return ((Yts, YtsSD, Yerr))

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def get_T(x, hasSlp, hasTOrder):
    c = np.concatenate
    Y = x.trend.Y;
    tmp = Y + x.trend.SD;
    SD = c( [Y - x.trend.SD, np.flip(tmp)] )
    if isfield(x.trend, 'CI') and not isempty(x.trend.CI):
        tmp = x.trend.CI[:,1]
        CI  = c( [x.trend.CI[:, 0], np.flip(tmp) ])
    else:
        CI = SD
    if (hasSlp):
        Slp   = x.trend.slp;
        tmp   = Slp + x.trend.slpSD;
        SlpSD = c( [Slp - x.trend.slpSD, np.flip(tmp) ] )
        SlpSignPos = x.trend.slpSgnPosPr;
        SlpSignZero = x.trend.slpSgnZeroPr;
    else:
        Slp = [];
        SlpSD = [];
        SlpSignPos = [];
        SlpSignZero = [];

    if (hasTOrder):
        Order = x.trend.order;
    else:
        Order = [];
    return (Y, SD, CI, Slp, SlpSD, SlpSignPos, SlpSignZero, Order)

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def get_tcp(x, ncpStat):
    cmpnt, cp, cpCI = (x.trend, x.trend.cp,x.trend.cpCI)

    if    ncpStat == 'mode':
        ncp = cmpnt.ncp_mode;
    elif  ncpStat == 'median':
        ncp = cmpnt.ncp_median;
    elif  ncpStat == 'mean':
        ncp = cmpnt.ncp;
    elif  ncpStat == 'pct90':
        ncp = cmpnt.ncp_pct90;
    elif ncpStat == 'pct10':
        ncp = cmpnt.ncp_pct10;
    elif ncpStat == 'max':
        ncp = sum(~np.isnan(cp));
    else:
        ncp = cmpnt.ncp_mode;

    ncp  = int( np.round(ncp) );
    ncpPr, cpPr,cpChange, Prob = (cmpnt.ncpPr, cmpnt.cpPr ,cmpnt.cpAbruptChange, cmpnt.cpOccPr)
    Prob1 = c( [Prob,Prob - Prob])

    #% %  ###########################################################
    return (cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1)


def get_S(x, hasAmp, hasSOrder):
    Y = x.season.Y;
    tmp = Y + x.season.SD;
    SD = c( [Y - x.season.SD, np.flip(tmp)])

    if isfield(x.season, 'CI') and not isempty(x.season.CI):
        tmp = x.season.CI[:, 1];
        CI = c( [x.season.CI[:, 0],  np.flip(tmp)] )
    else:
        CI = SD

    if hasAmp:
        Amp = x.season.amp;
        tmp   = Amp + x.season.ampSD;
        AmpSD = c( [Amp - x.season.ampSD,  np.flip(tmp) ])
    else:
        Amp = [];
        AmpSD = [];

    if hasSOrder:
        Order = x.season.order;
    else:
        Order = [];
    return (Y, SD, CI, Amp, AmpSD, Order)

#% %  ###########################################################
def get_O(x):
    Y   = x.outlier.Y
    SD = c( [Y - x.outlier.SD,  np.flip(Y + x.outlier.SD) ])

    if isfield(x.outlier, 'CI') and not isempty(x.outlier.CI):
        CI = c( [x.outlier.CI[:,0], np.flip(x.outlier.CI[:, 1]) ] )
    else:
        CI = SD
    return (Y, SD, CI)

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def get_scp(x, ncpStat):
    cmpnt, cp, cpCI = (x.season, x.season.cp,x.season.cpCI)

    if    ncpStat == 'mode':
        ncp = cmpnt.ncp_mode;
    elif  ncpStat == 'median':
        ncp = cmpnt.ncp_median;
    elif  ncpStat == 'mean':
        ncp = cmpnt.ncp;
    elif  ncpStat == 'pct90':
        ncp = cmpnt.ncp_pct90;
    elif ncpStat == 'pct10':
        ncp = cmpnt.ncp_pct10;
    elif ncpStat == 'max':
        ncp = sum(~np.isnan(cp));
    else:
        ncp = cmpnt.ncp_mode;

    ncp  = int( np.round(ncp) );
    ncpPr, cpPr,cpChange, Prob = (cmpnt.ncpPr, cmpnt.cpPr ,cmpnt.cpAbruptChange, cmpnt.cpOccPr)
    Prob1 = c( [Prob, Prob - Prob])
    #% %  ###########################################################
    return (cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1)

def  get_ocp(x, ncpStat):
    cmpnt, cp, cpCI = (x.outlier, x.outlier.cp,x.outlier.cpCI)

    if    ncpStat == 'mode':
        ncp = cmpnt.ncp_mode;
    elif  ncpStat == 'median':
        ncp = cmpnt.ncp_median;
    elif  ncpStat == 'mean':
        ncp = cmpnt.ncp;
    elif  ncpStat == 'pct90':
        ncp = cmpnt.ncp_pct90;
    elif ncpStat == 'pct10':
        ncp = cmpnt.ncp_pct10
    elif ncpStat == 'max':
        ncp = sum(~np.isnan(cp))
    else:
        ncp = cmpnt.ncp_mode

    ncp  = int( np.round(ncp) );
    ncpPr, cpPr,cpChange, Prob = (cmpnt.ncpPr, cmpnt.cpPr ,[], cmpnt.cpOccPr)
    Prob1 = c( [Prob, Prob - Prob])
    #% %  ###########################################################
    return (cp, cpCI, ncp, ncpPr, cpPr, cpChange, Prob, Prob1)

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def getylim(y):
    ymin,ymax = (np.min(y), np.max(y) )
    yext = ymax -ymin
    return (ymin - yext*0.1, ymax+yext*0.1)

def plot_st(h, ytitle, has, clr, x, t, t2t, Yts, YtsSD):
    alpha = 0.1;
    h.fill(t2t, YtsSD, alpha=0.3, facecolor=clr.copy(), linestyle='None');
    if has.hasData:
       h.plot(t, x.data, marker='o', color=clr);
    h.plot(t, Yts, color=clr,linestyle='solid',marker='None')
    h.set_ylim( getylim(YtsSD))

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_y(h, ytitle, has, clr, x, t, t2t, Y, CI, ncp, cp):
    alpha = 0.2;
    if (has.hasData  and not has.hasSeason):
        h.plot(t, x.data,  marker='o', color=[.5, .5, .5])
    h.fill(t2t, CI, facecolor=clr, alpha=alpha, linestyle='None');
    h.plot(t, Y, color= clr);
    ylim = h.get_ylim()
    for i in range(ncp):
        h.plot([cp[i], cp[i]], ylim, color='k');
    h.set_ylim(ylim)

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_prob(h, ytitle, has, clr, x, t, t2t, Prob1, Prob, ncp, cp):
    alpha = 0.2;
    h.fill( t2t, Prob1, color=clr, linestyle='None', alpha=alpha);
    h.plot(t, Prob, color=clr)
    maxp = np.min( [1, np.max(Prob) * 1.5])
    maxp = np.max([maxp, 0.2])
    h.set_ylim( (0, maxp) )

    for i in range(ncp):
        h.plot([cp[i], cp[i] ], h.get_ylim(), color='k')

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_order(h, ytitle, has, clr, x, t, t2t, Order, ncp, cp):
    h.plot(t, Order, color=clr);
    maxp = np.max([ np.max(Order), 1.05]);
    minp = -0.05;
    h.set_ylim([minp, maxp])
    for i in range(ncp):
        h.plot([cp[i], cp[i]], h.get_ylim(), color='k')

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_amp(h, ytitle, has, clr, x, t, t2t, Amp, AmpSD):
    alpha = 0.5;
    #% $fill(t2t, AmpSD, col=rgb(col[1], col[2], col[3], alpha), border=NA);
    h.plot(t, Amp, color=clr);

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_slp(h, ytitle, has, clr, x, t, t2t, Slp, SlpSD):
    alpha = 0.5;
    h.fill(t2t, SlpSD, color=clr, Linestyle='None', alpha=alpha)
    h.plot(t, Slp, color=clr)

#% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
def plot_slpsgn(h, ytitle, has, clr, x, t, t2t, SlpSignPos, SlpSignZero):
    alpha      = 0.5;
    SlpSignNeg = 1 - SlpSignPos - SlpSignZero;
    y2y        = c( [t - t,  np.flip( SlpSignNeg ) ] )
    h.fill(t2t, y2y, color=[0, 0, 1], linestyle='None', alpha=alpha);
    y2y = c( [SlpSignNeg,  1 - np.flip( SlpSignPos) ] )
    h.fill(t2t, y2y, color=[0, 1, 0], linestyle='None', alpha=alpha);
    y2y = c( [1 - SlpSignPos, t - t + 1])
    h.fill(t2t, y2y, color=[1, 0, 0], linestyle='None', alpha=alpha);
    h.plot(t, t - t + 0.5);

def plot_o(h, ytitle, has, clr, x, t, t2t, Y, CI, ncp, cp):
    alpha = 0.5;
    #%  # polygon(t2t, CI,   col  = rgb(col[1],col[2],col[3],alpha), border = NA);
    #$%  # points( t,   Y,    type = 'l',col='#333333');
    h.stem( t, Y,  linefmt='-', markerfmt=None ,use_line_collection=True)

def plot_oprob(h, ytitle, has, clr, x, t, t2t, Prob1, Prob, ncp, cp):
    alpha = 0.2
    #% plot(c(t2t[1], t2t), c(0.22, Prob1), type='n', ann=FALSE, xaxt='n', yaxt='n');
   #%  # polygon(t2t, Prob1, col  = rgb(col[1],col[2],col[3],alpha), border = NA);
   # %  # points( t,   Prob,  col  = rgb(col[1],col[2],col[3])  ,       lwd = 1,type = 'l' );
    h.stem(t, Prob,  linefmt='-', markerfmt=None,use_line_collection=True)

def plot_error(h, ytitle, has, clr, x, t, t2t, Yerr):
    #% plot(t, Yerr, type='n', ann=FALSE, xaxt='n', yaxt='n');
    h.plot(t, t - t, color=clr);
    h.stem(t, Yerr, linefmt='-', markerfmt=None,use_line_collection=True)
