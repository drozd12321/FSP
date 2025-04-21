import { watch } from "vue";
import { useField, useForm } from "vee-validate";
import { computed } from "vue";
import * as yup from "yup";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default function useLoginForm() {
  const router = useRouter();
  const store = useStore();
  const validationSchema = yup.object({
    email: yup
      .string()
      .trim()
      .required("Введите email")
      .email("Введите корректный email"),
    password: yup
      .string()
      .trim()
      .required("Введите пароль")
      .min(6, "Минимум 8 символов "),
    name: yup.string().trim().required("Введите имя").min(3),
    firstname: yup.string().trim().required("Введите фамилию").min(3),
    lastname: yup.string().trim(),
    nickname: yup.string().trim().required("Введите пароль").min(2),
    status: yup.string().trim().required("Выберите статус регистрации"),
    dt: yup.string().trim().required("Введите Дату Рождения").min(6),
    region: yup.string().trim().required("Выберите регион"),
  });
  const { handleSubmit, isSubmitting, submitCount, resetForm } = useForm({
    validationSchema,
    initialValues: {
      email: "",
      password: "",
      name: "",
      firstname: "",
      lastname: "",
      nickname: "",
      status: "",
      dt: "",
      region: "",
    },
  });
  const {
    value: email,
    errorMessage: emailError,
    handleBlur: emailBlur,
  } = useField("password");
  const {
    value: password,
    errorMessage: passwordError,
    handleBlur: passwordBlur,
  } = useField("password");
  const {
    value: name,
    errorMessage: nameError,
    handleBlur: nameBlur,
  } = useField("password");
  const {
    value: firstname,
    errorMessage: firstnameError,
    handleBlur: firstnameBlur,
  } = useField("password");
  const {
    value: lastname,
    errorMessage: lastnameError,
    handleBlur: lastnameBlur,
  } = useField("password");
  const {
    value: nickname,
    errorMessage: nicknameError,
    handleBlur: nicknameBlur,
  } = useField("password");
  const {
    value: status,
    errorMessage: statusError,
    handleBlur: statusBlur,
  } = useField("password");
  const {
    value: dt,
    errorMessage: dtError,
    handleBlur: dtBlur,
  } = useField("password");
  const {
    value: region,
    errorMessage: regionError,
    handleBlur: regionBlur,
  } = useField < string > "email";
  const onSubmit = handleSubmit(async (val) => {
    await store.dispatch("auth/login", val);
    router.push("/");
    resetForm();
  });
  const istomanyAttemots = computed < boolean > (() => submitCount.value >= 3);
  watch(istomanyAttemots, (val) => {
    if (val) {
      setTimeout(() => {
        submitCount.value = 0;
      }, 4000);
    }
  });
  return {
    nicknameBlur,
    nicknameBlur,
    nicknameError,
    email,
    password,
    name,
    nickname,
    firstname,
    lastname,
    status,
    dt,
    region,
    onSubmit,
    istomanyAttemots,
    firstnameBlur,
    firstnameError,
    emailBlur,
    emailError,
    passwordBlur,
    passwordError,
    nameBlur,
    nameError,
    lastnameBlur,
    lastnameError,
    firstnameBlur,
    firstnameError,
    statusBlur,
    statusError,
    dtBlur,
    dtError,
    regionBlur,
    regionError,
  };
}
