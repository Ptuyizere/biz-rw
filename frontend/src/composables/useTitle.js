import { watch, onUnmounted } from 'vue'

const BASE_TITLE = 'biz.rw'

export function useTitle(title) {
  function setTitle(val) {
    document.title = val ? `${val} — ${BASE_TITLE}` : BASE_TITLE
  }

  if (typeof title === 'string') {
    setTitle(title)
  } else {
    // reactive ref/computed
    watch(title, (val) => setTitle(val), { immediate: true })
  }

  onUnmounted(() => {
    document.title = BASE_TITLE
  })
}
