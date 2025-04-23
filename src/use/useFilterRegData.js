export default function formatRegDate(dateString) {
  const date = new Date(dateString);

  if (isNaN(date.getTime())) {
    return "Неверная дата";
  }

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

  const day = date.getDate();
  const month = months[date.getMonth()];
  const year = date.getFullYear();

  return `${day} ${month} ${year} года`;
}
