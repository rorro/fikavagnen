import constants

def is_command(msg):
    return msg.startswith("!")


def parse_command(msg):
    split_msg = msg[1:].split()

    cmd = split_msg[0]
    args = split_msg[1:]

    return cmd, args


def is_valid_command(cmd):
    return cmd in constants.COMMANDS


def is_valid_metric(metric):
    return metric in constants.METRICS


def metric_to_emoji(metric):
    if metric == "tea":
        return "🍵"
    elif metric == "coffee":
        return "☕"
    elif metric == "thanks":
        return "🙏"
    elif metric == "thanks_at":
        return "@🙏"
    elif metric == "no_thanks":
        return "🙄"
    else:
        return metric

def emoji_to_metric(emoji):
    if emoji == "🍵":
        return "tea"
    elif emoji == "☕":
        return "coffee"
    elif emoji == "🙏":
        return "thanks"
    elif emoji == "@🙏":
        return "thanks_at"
    elif emoji == "🙄":
        return "no_thanks"
    else:
        return emoji
