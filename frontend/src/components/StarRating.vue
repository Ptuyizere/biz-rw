<template>
  <div class="flex items-center gap-1">
    <button
      v-for="i in 5"
      :key="i"
      type="button"
      @click="!readonly && emit('update:modelValue', i)"
      @mouseover="!readonly && (hovered = i)"
      @mouseleave="!readonly && (hovered = 0)"
      :disabled="readonly"
      class="transition-all duration-100 focus:outline-none"
      :class="[
        readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110',
        sizeClass
      ]"
    >
      <span :class="starColor(i)">★</span>
    </button>
    <span v-if="showCount && count !== undefined" class="ml-1 text-sm text-gray-400">({{ count }})</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 0 },
  readonly: { type: Boolean, default: false },
  size: { type: String, default: 'md' }, // sm | md | lg
  showCount: { type: Boolean, default: false },
  count: { type: Number, default: undefined },
})

const emit = defineEmits(['update:modelValue'])
const hovered = ref(0)

const sizeClass = {
  sm: 'text-base',
  md: 'text-xl',
  lg: 'text-3xl',
}[props.size] || 'text-xl'

function starColor(i) {
  const active = hovered.value ? i <= hovered.value : i <= props.modelValue
  return active ? 'text-rw-gold-400' : 'text-gray-200'
}
</script>
