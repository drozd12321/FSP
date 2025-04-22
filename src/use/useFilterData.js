export default function formatDateRange(dateStringStart, dateStringEnd) {
  const months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
  ];
  const startDate = new Date(dateStringStart);
  const endDate = new Date(dateStringEnd);

  return `${startDate.getDate()} ${
    months[startDate.getMonth()]
  } - ${endDate.getDate()} ${months[endDate.getMonth()]}`;
}
