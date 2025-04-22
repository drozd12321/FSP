const validateForm = () => {
  const errors = [];
  if (!form.value.name.trim()) {
    errors.push("Название команды обязательно для заполнения.");
  }
  if (comand.value !== "0" && comand.value !== "1") {
    errors.push("Выберите корректный вид команды (Публичная или Приватная).");
  }
  if (form.value.description.length > 500) {
    errors.push("Описание не должно превышать 500 символов.");
  }
  return errors;
};
export default validateForm;
