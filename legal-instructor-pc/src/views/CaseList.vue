<template>
  <div class="case-list-container">
    <div class="header">
      <h1>案例列表</h1>
      <el-button type="primary" @click="goToCreate">
        <el-icon><Plus /></el-icon>
        录入新案例
      </el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索案例标题或副标题"
        style="width: 400px"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 案例列表 -->
    <div class="case-list" v-loading="loading">
      <el-empty v-if="!loading && cases.length === 0" description="暂无案例" />
      
      <div
        v-for="caseItem in cases"
        :key="caseItem.id"
        class="case-card"
        @click="viewCaseDetail(caseItem.id)"
      >
        <div class="case-header">
          <h3 class="case-title">{{ caseItem.title }}</h3>
          <div class="case-actions" @click.stop>
            <el-button
              type="primary"
              text
              @click="editCase(caseItem.id)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              text
              @click="deleteCase(caseItem.id)"
            >
              删除
            </el-button>
          </div>
        </div>
        
        <div class="case-subtitle">{{ caseItem.subtitle }}</div>
        
        <div class="case-info">
          <el-tag v-for="(keyword, index) in caseItem.keywords.slice(0, 3)" :key="index" size="small">
            {{ typeof keyword === 'object' ? keyword.value : keyword }}
          </el-tag>
        </div>
        
        <div class="case-meta">
          <span class="case-time">
            <el-icon><Clock /></el-icon>
            {{ formatDate(caseItem.created_at) }}
          </span>
          <span class="case-count">
            <el-icon><Document /></el-icon>
            {{ caseItem.dispute_foci?.length || 0 }} 个争议焦点
          </span>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchCases"
        @current-change="fetchCases"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Clock, Document } from '@element-plus/icons-vue'
import { getCases, deleteCase as deleteCaseApi } from '@/api/case'

const router = useRouter()
const loading = ref(false)
const cases = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')

onMounted(() => {
  fetchCases()
})

function fetchCases() {
  loading.value = true
  getCases({
    keyword: searchKeyword.value,
    page: currentPage.value,
    page_size: pageSize.value
  }).then(res => {
    if (res.success) {
      cases.value = res.data.cases
      total.value = res.data.total
    } else {
      ElMessage.error('获取案例列表失败')
    }
  }).finally(() => {
    loading.value = false
  })
}

function handleSearch() {
  currentPage.value = 1
  fetchCases()
}

function goToCreate() {
  router.push('/case-input')
}

function viewCaseDetail(id) {
  router.push(`/case-detail/${id}`)
}

function editCase(id) {
  router.push(`/case-input?id=${id}`)
}

function deleteCase(id) {
  ElMessageBox.confirm(
    '确定要删除这个案例吗？删除后无法恢复。',
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    deleteCaseApi(id).then(res => {
      if (res.success) {
        ElMessage.success('删除成功')
        fetchCases()
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
.case-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #1F2937;
  font-weight: 600;
}

.search-bar {
  margin-bottom: 30px;
}

.case-list {
  min-height: 400px;
}

.case-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.case-card:hover {
  border-color: #4F46E5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.case-title {
  font-size: 18px;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
  flex: 1;
  margin-right: 20px;
}

.case-actions {
  display: flex;
  gap: 8px;
}

.case-subtitle {
  font-size: 14px;
  color: #6B7280;
  margin-bottom: 16px;
  line-height: 1.5;
}

.case-info {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.case-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #9CA3AF;
}

.case-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
