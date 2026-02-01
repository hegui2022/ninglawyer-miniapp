<template>
  <div class="rich-text-editor">
    <div class="toolbar">
      <button
        v-for="tool in toolbarTools"
        :key="tool.key"
        :class="['toolbar-btn', { active: isToolActive(tool.key) }]"
        @click="handleToolClick(tool.key)"
        :title="tool.title"
      >
        {{ tool.label }}
      </button>
    </div>
    <div
      ref="editorRef"
      class="editor-content"
      contenteditable="true"
      @input="handleInput"
      @blur="handleBlur"
      :placeholder="placeholder"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '请输入内容...'
  }
})

const emit = defineEmits(['update:modelValue'])

const editorRef = ref(null)

const toolbarTools = [
  { key: 'bold', label: 'B', title: '加粗' },
  { key: 'italic', label: 'I', title: '斜体' },
  { key: 'underline', label: 'U', title: '下划线' },
  { key: 'strikeThrough', label: 'S', title: '删除线' },
  { key: 'foreColor', label: 'A', title: '字体颜色' },
  { key: 'hiliteColor', label: '🖊', title: '背景色' },
  { key: 'fontSize', label: 'Size', title: '字号' },
  { key: 'formatBlock', label: 'H', title: '标题' },
  { key: 'justifyLeft', label: '左', title: '左对齐' },
  { key: 'justifyCenter', label: '中', title: '居中对齐' },
  { key: 'justifyRight', label: '右', title: '右对齐' },
  { key: 'insertOrderedList', label: 'OL', title: '有序列表' },
  { key: 'insertUnorderedList', label: 'UL', title: '无序列表' },
  { key: 'indent', label: '→', title: '增加缩进' },
  { key: 'outdent', label: '←', title: '减少缩进' },
  { key: 'undo', label: '↩', title: '撤销' },
  { key: 'redo', label: '↪', title: '重做' }
]

onMounted(() => {
  if (editorRef.value && props.modelValue) {
    editorRef.value.innerHTML = props.modelValue
  }
})

watch(() => props.modelValue, (newVal) => {
  if (editorRef.value && newVal !== editorRef.value.innerHTML) {
    editorRef.value.innerHTML = newVal
  }
})

function handleInput() {
  emit('update:modelValue', editorRef.value.innerHTML)
}

function handleBlur() {
  emit('update:modelValue', editorRef.value.innerHTML)
}

function handleToolClick(tool) {
  editorRef.value.focus()
  
  // 特殊工具处理
  if (tool === 'foreColor') {
    const color = prompt('请输入颜色值（如：#FF0000 或 red）', '#000000')
    if (color) {
      document.execCommand('foreColor', false, color)
    }
  } else if (tool === 'hiliteColor') {
    const color = prompt('请输入背景色值（如：#FFFF00 或 yellow）', '#FFFF00')
    if (color) {
      document.execCommand('hiliteColor', false, color)
    }
  } else if (tool === 'fontSize') {
    const size = prompt('请输入字号（1-7）', '3')
    if (size) {
      document.execCommand('fontSize', false, size)
    }
  } else if (tool === 'formatBlock') {
    const format = prompt('请输入格式（h1/h2/h3/p）', 'p')
    if (format) {
      document.execCommand('formatBlock', false, format)
    }
  } else {
    // 常规工具
    document.execCommand(tool, false, null)
  }
}

function isToolActive(tool) {
  return document.queryCommandState(tool)
}
</script>

<style scoped>
.rich-text-editor {
  border: 1px solid #E5E7EB;
  border-radius: 4px;
  overflow: hidden;
}

.toolbar {
  display: flex;
  gap: 5px;
  padding: 8px;
  background: #F9FAFB;
  border-bottom: 1px solid #E5E7EB;
  flex-wrap: wrap;
}

.toolbar-btn {
  min-width: 30px;
  height: 30px;
  border: 1px solid #D1D5DB;
  background: white;
  border-radius: 3px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #F3F4F6;
}

.toolbar-btn.active {
  background: #4F46E5;
  color: white;
  border-color: #4F46E5;
}

.editor-content {
  min-height: 200px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.6;
  overflow-y: auto;
}

.editor-content:empty::before {
  content: attr(placeholder);
  color: #9CA3AF;
  font-style: italic;
}

.editor-content:focus {
  outline: none;
}
</style>
