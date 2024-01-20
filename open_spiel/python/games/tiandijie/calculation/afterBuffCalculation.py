def before_buff_calculation(buffs):
    buffs[:] = [buff for buff in buffs if buff.duration > 0]
