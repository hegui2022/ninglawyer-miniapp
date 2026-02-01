<template>
  <div class="case-input-container">
    <div class="header">
      <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
      <h1>{{ isEditMode ? '编辑案例' : '法律案例录入' }}</h1>
    </div>

    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px" v-loading="loading">
      <!-- 模块1：基础信息区 -->
      <div class="form-section">
        <div class="section-title">基础信息</div>
        
        <el-form-item label="标题" prop="title" required>
          <el-input
            v-model="formData.title"
            placeholder="刑事: 如张某盗窃案；民事: 如张三诉李四侵害商标权纠纷案"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="副标题" prop="subtitle" required>
          <el-input
            v-model="formData.subtitle"
            placeholder="反映参考案例的精髓、核心"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="关键词" prop="keywords" required>
          <div class="keywords-container">
            <el-select
              v-model="formData.keywords[0].value"
              placeholder="请选择：裁判类型"
              style="width: 200px; margin-right: 10px"
            >
              <el-option label="判决" value="判决" />
              <el-option label="裁定" value="裁定" />
              <el-option label="调解" value="调解" />
            </el-select>

            <el-select
              v-model="formData.keywords[1].value"
              placeholder="请选择：案由"
              style="width: 200px; margin-right: 10px"
            >
              <el-option label="盗窃" value="盗窃" />
              <el-option label="故意伤害" value="故意伤害" />
              <el-option label="离婚" value="离婚" />
              <el-option label="合同纠纷" value="合同纠纷" />
              <el-option label="劳动争议" value="劳动争议" />
            </el-select>

            <el-input
              v-for="(keyword, index) in formData.keywords.slice(2)"
              :key="index"
              v-model="keyword.value"
              placeholder="请输入关键词"
              style="width: 200px; margin-right: 10px"
            />
          </div>
        </el-form-item>
      </div>

      <!-- 模块2：基本案情区 -->
      <div class="form-section">
        <div class="section-title">基本案情 <span class="required">*</span></div>
        <RichTextEditor
          v-model="formData.basic_facts"
          placeholder="xxx诉称: ......\nxxx辩称: ......\n(分别阐述原、告诉辩意见及其主要理由)\n法院经审理查明: ......(准确概述审理查明事实，一般不具具体证据，但与案例所要解决的问题有密切联系的，在查明事实之后出具具体证据，与案例总结的裁判要旨相关的事实、情节和法律适用问题，要有针对性地详加阐述。)"
        />
      </div>

      <!-- 模块3：裁判要旨区 -->
      <div class="form-section">
        <div class="section-title">裁判要旨 <span class="required">*</span></div>
        <RichTextEditor
          v-model="formData.judgment_essence"
          placeholder="......（裁判要旨是整个案例拟解决问题的概要表述，应简要归纳和提炼参考案例体现的具体类案参考、指引作用的裁判规则、理念或方法等，以及审理类似案件应当注意的问题。裁判要旨阐释提炼的规则、理念、方法等，为两个以上的，按照裁判要旨的重要性或者逻辑关系用阿拉伯数字标示。）"
        />
      </div>

      <!-- 模块4：裁判结果区 -->
      <div class="form-section">
        <div class="section-title">裁判结果 <span class="required">*</span></div>
        <RichTextEditor
          v-model="formData.judgment_result"
          placeholder="xxx法院于xxxx年xx月xx日作出xxx号（写明案号）刑事（民事、行政等）判决（裁定等）......(写明裁判结果)。\n宣判后，xxx提出上诉（未提出上诉，判决已发生法律效力）。xxx法院于xxxx年xx月xx日作出xxx号（写明案号）刑事（民事、行政等）判决（裁定等），驳回上诉，维持原判。（二审改判、发回重审的，根据需要确定是否写明改判、发挥重审的简要理由和情况。再审的写明再审的简要理由和情况。）"
        />
      </div>

      <!-- 模块5：关联索引区 -->
      <div class="form-section">
        <div class="section-title">关联索引 <span class="required">*</span></div>

        <!-- 主要法条 -->
        <div class="subsection">
          <div class="subsection-title">主要法条</div>
          <div
            v-for="(law, index) in formData.related_index.laws"
            :key="index"
            class="law-item"
          >
            <el-input
              v-model="law.law_name"
              placeholder="请输入：法律名称，如《中华人民共和国刑法》"
              style="width: 400px; margin-right: 10px"
            />
            <el-input
              v-model="law.article_numbers"
              placeholder="请输入：法条序号，用顿号隔开，如第1条、第2条"
              style="width: 400px"
            />
            <el-button
              v-if="formData.related_index.laws.length > 1"
              type="danger"
              text
              @click="removeLaw(index)"
              style="margin-left: 10px"
            >
              ×
            </el-button>
          </div>
          <el-button
            type="primary"
            text
            @click="addLaw"
            style="margin-top: 10px"
          >
            + 添加法条
          </el-button>
        </div>

        <!-- 历审程序 -->
        <div class="subsection" style="margin-top: 30px">
          <div class="subsection-title">历审程序</div>
          <div
            v-for="(proc, index) in formData.related_index.proceedings"
            :key="index"
            class="proceeding-item"
          >
            <el-select
              v-model="proc.procedure_type"
              placeholder="请选择：审理程序"
              style="width: 150px; margin-right: 10px"
            >
              <el-option label="一审" value="一审" />
              <el-option label="二审" value="二审" />
              <el-option label="再审" value="再审" />
            </el-select>

            <el-select
              v-model="proc.court"
              placeholder="请选择：审理法院"
              style="width: 200px; margin-right: 10px"
            >
              <el-option label="基层法院" value="基层法院" />
              <el-option label="中级法院" value="中级法院" />
              <el-option label="高级法院" value="高级法院" />
              <el-option label="最高人民法院" value="最高人民法院" />
            </el-select>

            <el-input
              v-model="proc.case_number"
              placeholder="请输入：案号"
              style="width: 200px; margin-right: 10px"
            />
            <el-input
              v-model="proc.judgment_type"
              placeholder="请输入：裁判类型"
              style="width: 150px; margin-right: 10px"
            />
            <el-date-picker
              v-model="proc.judgment_date"
              type="date"
              placeholder="请输入：裁判日期"
              style="width: 200px; margin-right: 10px"
            />
            <el-button
              type="danger"
              text
              @click="removeProceeding(index)"
            >
              ×
            </el-button>
          </div>
          <el-button
            type="primary"
            text
            @click="addProceeding"
            style="margin-top: 10px"
          >
            + 添加历审程序
          </el-button>
        </div>
      </div>

      <!-- 模块6：争议焦点区 -->
      <div class="form-section">
        <div class="section-title">争议焦点 <span class="required">*</span></div>
        <div
          v-for="(focus, index) in formData.dispute_foci"
          :key="index"
          class="dispute-focus-item"
        >
          <el-input
            v-model="formData.dispute_foci[index]"
            placeholder="请输入争议焦点内容，如'合同效力是否有效'"
            style="width: 400px; margin-right: 10px"
          />
          <el-button
            v-if="formData.dispute_foci.length > 1"
            type="danger"
            text
            @click="removeDisputeFocus(index)"
          >
            ×
          </el-button>
        </div>
        <el-button
          type="primary"
          text
          @click="addDisputeFocus"
          style="margin-top: 10px"
        >
          + 添加争议焦点
        </el-button>
      </div>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <el-button type="primary" size="large" @click="handleSubmit" :loading="submitting">
          {{ isEditMode ? '保存修改' : '提交案例' }}
        </el-button>
        <el-button size="large" @click="handleReset" :disabled="isEditMode">
          重置表单
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import RichTextEditor from '@/components/RichTextEditor.vue'
import { createCase, updateCase, getCaseDetail } from '@/api/case'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)
const loading = ref(false)
const caseId = computed(() => route.query.id)
const isEditMode = computed(() => !!caseId.value)

// 表单数据
const formData = reactive({
  title: '',
  subtitle: '',
  keywords: [
    { type: '裁判类型', value: '' },
    { type: '案由', value: '' },
    { value: '' },
    { value: '' },
    { value: '' }
  ],
  basic_facts: '',
  judgment_essence: '',
  judgment_result: '',
  dispute_foci: ['', ''],
  related_index: {
    laws: [{ law_name: '', article_numbers: '' }],
    proceedings: [
      {
        procedure_type: '',
        court: '',
        case_number: '',
        judgment_type: '',
        judgment_date: null
      }
    ]
  }
})

// 表单验证规则
const formRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  subtitle: [{ required: true, message: '请输入副标题', trigger: 'blur' }]
}

// 页面加载时检查是否为编辑模式
onMounted(() => {
  if (isEditMode.value) {
    loadCaseData(caseId.value)
  }
})

// 加载案例数据
async function loadCaseData(id) {
  loading.value = true
  try {
    const res = await getCaseDetail(id)
    if (res.success) {
      const data = res.data
      
      // 填充表单数据
      formData.title = data.title
      formData.subtitle = data.subtitle
      formData.keywords = data.keywords || [
        { type: '裁判类型', value: '' },
        { type: '案由', value: '' },
        { value: '' },
        { value: '' },
        { value: '' }
      ]
      formData.basic_facts = data.basic_facts || ''
      formData.judgment_essence = data.judgment_essence || ''
      formData.judgment_result = data.judgment_result || ''
      formData.dispute_foci = data.dispute_foci || ['', '']
      formData.related_index = {
        laws: data.laws || [{ law_name: '', article_numbers: '' }],
        proceedings: data.proceedings || [
          {
            procedure_type: '',
            court: '',
            case_number: '',
            judgment_type: '',
            judgment_date: null
          }
        ]
      }
    } else {
      ElMessage.error('加载案例数据失败')
      goBack()
    }
  } catch (error) {
    console.error('加载案例数据失败:', error)
    ElMessage.error('加载案例数据失败')
    goBack()
  } finally {
    loading.value = false
  }
}

// 返回列表
function goBack() {
  router.push('/case-list')
}

// 添加法条
function addLaw() {
  formData.related_index.laws.push({ law_name: '', article_numbers: '' })
}

// 删除法条
function removeLaw(index) {
  formData.related_index.laws.splice(index, 1)
}

// 添加历审程序
function addProceeding() {
  formData.related_index.proceedings.push({
    procedure_type: '',
    court: '',
    case_number: '',
    judgment_type: '',
    judgment_date: null
  })
}

// 删除历审程序
function removeProceeding(index) {
  formData.related_index.proceedings.splice(index, 1)
}

// 添加争议焦点
function addDisputeFocus() {
  formData.dispute_foci.push('')
}

// 删除争议焦点
function removeDisputeFocus(index) {
  formData.dispute_foci.splice(index, 1)
}

// 提交表单
async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请填写必填项')
      return
    }

    // 验证其他必填项
    if (!formData.basic_facts || !formData.judgment_essence || !formData.judgment_result) {
      ElMessage.error('请填写基本案情、裁判要旨和裁判结果')
      return
    }

    if (formData.dispute_foci.some(f => !f.trim())) {
      ElMessage.error('请填写所有争议焦点')
      return
    }

    // 过滤空的关键词
    const filteredKeywords = formData.keywords.filter(k => k.value && k.value.trim())

    submitting.value = true

    try {
      const submitData = {
        title: formData.title,
        subtitle: formData.subtitle,
        keywords: filteredKeywords,
        basic_facts: formData.basic_facts,
        judgment_essence: formData.judgment_essence,
        judgment_result: formData.judgment_result,
        dispute_foci: formData.dispute_foci.filter(f => f.trim()),
        related_index: {
          laws: formData.related_index.laws.filter(l => l.law_name && l.law_name.trim()),
          proceedings: formData.related_index.proceedings.filter(p => p.case_number && p.case_number.trim())
        },
        status: 'published',
        created_by: 'legal_instructor'
      }

      if (isEditMode.value) {
        // 更新模式
        await updateCase(caseId.value, submitData)
        ElMessage.success('案例更新成功')
      } else {
        // 新增模式
        await createCase(submitData)
        ElMessage.success('案例提交成功')
      }

      // 跳转到列表页
      goBack()

    } catch (error) {
      console.error('提交失败:', error)
      ElMessage.error('提交失败: ' + (error.message || '未知错误'))
    } finally {
      submitting.value = false
    }
  })
}

// 重置表单
function handleReset() {
  if (isEditMode.value) {
    return // 编辑模式下不允许重置
  }
  
  formRef.value?.resetFields()
  formData.title = ''
  formData.subtitle = ''
  formData.keywords = [
    { type: '裁判类型', value: '' },
    { type: '案由', value: '' },
    { value: '' },
    { value: '' },
    { value: '' }
  ]
  formData.basic_facts = ''
  formData.judgment_essence = ''
  formData.judgment_result = ''
  formData.dispute_foci = ['', '']
  formData.related_index = {
    laws: [{ law_name: '', article_numbers: '' }],
    proceedings: [
      {
        procedure_type: '',
        court: '',
        case_number: '',
        judgment_type: '',
        judgment_date: null
      }
    ]
  }
}
</script>

<style scoped>
.case-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 28px;
  color: #1F2937;
  font-weight: 600;
  margin: 0;
}

.form-section {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #F3F4F6;
}

.required {
  color: #EF4444;
  font-size: 14px;
  margin-left: 5px;
}

.keywords-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.subsection {
  margin-top: 20px;
}

.subsection-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 15px;
}

.law-item,
.proceeding-item,
.dispute-focus-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding: 20px;
  background: white;
  border-radius: 8px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner) {
  border-radius: 4px;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-textarea__inner:focus) {
  border-color: #4F46E5;
  box-shadow: 0 0 0 1px #4F46E5;
}
</style>
