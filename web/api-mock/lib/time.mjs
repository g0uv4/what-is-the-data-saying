const TAIPEI = 'Asia/Taipei';

export function formatTaipei(date) {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: TAIPEI,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hourCycle: 'h23',
  }).formatToParts(date);
  const pick = (type) => parts.find((part) => part.type === type)?.value;
  return `${pick('year')}-${pick('month')}-${pick('day')}T${pick('hour')}:${pick('minute')}:${pick('second')}+08:00`;
}

export function taipeiDateKey(date) {
  return formatTaipei(date).slice(0, 10);
}

export function nextTaipeiMidnight(date) {
  const [year, month, day] = taipeiDateKey(date).split('-').map(Number);
  // 下一個台北 00:00 等於「當天 16:00 UTC」再加一天。
  const utcMidnight = Date.UTC(year, month - 1, day, 16, 0, 0);
  return new Date(utcMidnight);
}

export function addDaysTaipei(date, days) {
  return new Date(date.getTime() + days * 24 * 60 * 60 * 1000);
}

export function secondsUntil(later, now) {
  return Math.max(0, Math.ceil((later.getTime() - now.getTime()) / 1000));
}
