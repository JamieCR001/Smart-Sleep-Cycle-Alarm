def get_sleep_cycle(hr_values, alpha_hr):
  if not hr_values:
    return 0

  ema_hr = hr_values[0]
  for hr in hr_values[1:]:
    ema_hr = alpha_hr * hr + (1 - alpha_hr) * ema_hr

  current_hr = hr_values[-1]
  hr_diff = ema_hr - current_hr

  if hr_diff < -5:

    return 0
  elif 0 < hr_diff <= 5:
    return 1
  elif 5 < hr_diff <= 12:
    return 2
  elif hr_diff > 12:
    return 3
  else:

    return 2


def should_wake_up(sleep_cycle_number, strict_mode):

  if strict_mode:
    print("reached")
    if sleep_cycle_number < 2:
      return True
  else:
    if sleep_cycle_number < 3:
      return True

  return False