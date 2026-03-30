/**
 * Simple wrapper around window.confirm for now.
 * Can be replaced with a modal-based confirm in the future.
 */
export function useConfirm() {
  function confirm(message = 'Are you sure?') {
    return window.confirm(message)
  }

  return { confirm }
}
