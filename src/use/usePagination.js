import { ref } from "vue";
export function usePagination(initialPage = 1, totalPages = 1) {
  const currentPage = ref(initialPage);
  const pages = ref([]);
  const generatePages = () => {
    const result = [];
    for (let i = 1; i <= totalPages; i++) {
      result.push({
        number: i,
        isActive: i === currentPage.value,
      });
    }
    pages.value = result;
  };
  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) {
      currentPage.value = page;
      generatePages();
    }
  };
  const nextPage = () => {
    if (currentPage.value < totalPages) {
      currentPage.value++;
      generatePages();
    }
  };
  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
      generatePages();
    }
  };
  generatePages();
  return {
    currentPage,
    pages,
    goToPage,
    nextPage,
    prevPage,
    isFirstPage: () => currentPage.value === 1,
    isLastPage: () => currentPage.value === totalPages,
  };
}
