<template>
  <div class="case-detail-container" v-loading="loading">
    <div class="header">
      <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
      <h1>案例详情</h1>
      <div class="header-actions">
        <el-button type="primary" @click="editCase">编辑</el-button>
        <el-button type="danger" @click="deleteCase">删除</el-button>
      </div>
    </div>

    <div v-if="caseData" class="case-content">
      <!-- 基础信息 -->
      <div class="section">
        <h2 class="section-title">基础信息</h2>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="标题" :span="2">{{ caseData.title }}</el-descriptions-item>
          <el-descriptions-item label="副标题" :span="2">{{ caseData.subtitle }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="1">
            {{ formatDate(caseData.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="1">
            {{ formatDate(caseData.updated_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="关键词" :span="2">
            <el-tag
              v-for="(keyword, index) in caseData.keywords"
              :key="index"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ typeof keyword === 'object' ? `${keyword.type}: ${keyword.value}` : keyword }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 基本案情 -->
      <div class="section">
        <h2 class="section-title">基本案情</h2>
        <div class="html-content" v-html="caseData.basic_facts"></div>
      </div>

      <!-- 裁判要旨 -->
      <div class="section">
        <h2 class="section-title">裁判要旨</h2>
        <div class="html-content" v-html="caseData.judgment_essence"></div>
      </div>

      <!-- 裁判结果 -->
      <div class="section">
        <h2 class="section-title">裁判结果</h2>
        <div class="html-content" v-html="caseData.judgment_result"></div>
      </div>

      <!-- 争议焦点 -->
      <div class="section">
        <h2 class="section-title">争议焦点</h2>
        <el-timeline>
          <el-timeline-item
            v-for="(focus, index) in caseData.dispute_foci"
            :key="index"
            :color="'#4F46E5'"
          >
            {{ focus }}
          </el-timeline-item>
        </el-timeline>
      </div>

      <!-- 关联索引 -->
      <div class="section">
        <h2 class="section-title">关联索引</h2>
        
        <!-- 主要法条 -->
        <h3 class="subsection-title">主要法条</h3>
        <el-table :data="caseData.laws" border style="margin-bottom: 20px">
          <el-table-column type="index" label="序号" width="60" />
          <el-table-column prop="law_name" label="法律名称" />
          <el-table-column prop="article_numbers" label="法条" />
        </el-table>

        <!-- 历审程序 -->
        <h3 class="subsection-title">历审程序</h3>
        <el-timeline>
          <el-timeline-item
            v-for="(proc, index) in caseData.proceedings"
            :key="index"
            :timestamp="formatDate(proc.judgment_date)"
            placement="top"
          >
            <el-card>
              <h4>{{ proc.procedure_type }}</h4>
              <p><strong>法院：</strong>{{ proc.court }}</p>
              <p><strong>案号：</strong>{{ proc.case_number }}</p>
              <p><strong>裁判类型：</strong>{{ proc.judgment_type }}</p>
              <p><strong>裁判日期：</strong>{{ formatDate(proc.judgment_date) }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>

    <el-empty v-else-if="!loading" description="案例不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getCaseDetail, deleteCase as deleteCaseApi } from '@/api/case'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const caseData = ref(null)

onMounted(() => {
  loadCaseDetail()
})

function loadCaseDetail() {
  const id = route.params.id || route.query.id
  if (!id) {
    ElMessage.error('案例ID不存在')
    goBack()
    return
  }

  loading.value = true
  getCaseDetail(id).then(res => {
    if (res.success) {
      caseData.value = res.data
    } else {
      ElMessage.error('加载案例详情失败')
    }
  }).catch(() => {
    ElMessage.error('加载案例详情失败')
  }).finally(() => {
    loading.value = false
  })
}

function goBack() {
  router.back()
}

function editCase() {
  router.push(`/case-input?id=${caseData.value.id}`)
}

function deleteCase() {
  ElMessageBox.confirm(
    '确定要删除这个案例吗？删除后无法恢复。',
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    deleteCaseApi(caseData.value.id).then(res => {
      if (res.success) {
        ElMessage.success('删除成功')
        goBack()
      } else {
        ElMessage.error('删除失败')
      }
    })
  }).catch(() => {
    // 取消删除
  })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.case-detail-container {
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
  flex: 1;
  font-size: 28px;
  color: #1F2937;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.case-content {
  background: white;
}

.section {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1F2937;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #F3F4F6;
}

.subsection-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 20px 0 15px 0;
}

.html-content {
  line-height: 1.8;
  color: #374151;
}

.html-content :deep(p) {
  margin-bottom: 12px;
}

.html-content :deep(ul),
.html-content :deep(ol) {
  margin: 12px 0;
  padding-left: 24px;
}

.html-content :deep(li) {
  margin-bottom: 6px;
}

.html-content :deep(strong) {
  font-weight: 600;
  color: #1F2937;
}

:deep(.el-timeline-item__timestamp) {
  color: #6B7280;
  font-size: 14px;
}

:deep(.el-card) {
  background: #F9FAFB;
}

:deep(.el-card h4) {
  margin: 0 0 12px 0;
  color: #1F2937;
}

:deep(.el-card p) {
  margin: 8px 0;
  color: #6B7280;
}
</style>
