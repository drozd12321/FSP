import { watch } from "vue";
import { useField, useForm } from "vee-validate";
import { computed } from "vue";
import * as yup from "yup";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/useAuthStore";

export default function useLoginForm() {
  const router = useRouter();
  const authStore = useAuthStore();
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
      .min(8, "Минимум 8 символов "),
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
  } = useField("email");
  const {
    value: password,
    errorMessage: passwordError,
    handleBlur: passwordBlur,
  } = useField("password");
  const {
    value: name,
    errorMessage: nameError,
    handleBlur: nameBlur,
  } = useField("name");
  const {
    value: firstname,
    errorMessage: firstnameError,
    handleBlur: firstnameBlur,
  } = useField("firstname");
  const {
    value: lastname,
    errorMessage: lastnameError,
    handleBlur: lastnameBlur,
  } = useField("lastname");
  const {
    value: nickname,
    errorMessage: nicknameError,
    handleBlur: nicknameBlur,
  } = useField("nickname");
  const {
    value: status,
    errorMessage: statusError,
    handleBlur: statusBlur,
  } = useField("status");
  const {
    value: dt,
    errorMessage: dtError,
    handleBlur: dtBlur,
  } = useField("dt");
  const {
    value: region,
    errorMessage: regionError,
    handleBlur: regionBlur,
  } = useField("region");
  const onSubmit = handleSubmit(async (val) => {
    console.log("fff");
    console.log(val);
    await authStore.login();
    router.push("/");
    resetForm();
  });

  const istomanyAttemots = computed(() => submitCount.value >= 3);
  watch(istomanyAttemots, (val) => {
    if (val) {
      setTimeout(() => {
        submitCount.value = 0;
      }, 4000);
    }
  });
  return {
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
    isSubmitting,
    handleSubmit,
  };
}
