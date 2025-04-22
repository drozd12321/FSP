import axios from "axios";
import { ref } from "vue";
const comp = ref();
const getUser = async (token) => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/user-profile/", {
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });
    comp.value = response.data;
    console.log(comp.value);
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
export default getUser;
