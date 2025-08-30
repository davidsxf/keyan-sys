<!-- components/ProjectFormDialog.vue -->
<template>
  <el-dialog
    v-model="visible"
    :title="formTitle"
    width="600px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      label-position="right"
    >
      <el-form-item label="项目编号" prop="number">
        <el-input v-model="formData.number" placeholder="请输入项目编号" />
      </el-form-item>


      <el-form-item label="项目名称" prop="title">
        <el-input v-model="formData.title" placeholder="请输入项目名称" />
      </el-form-item>


      <el-form-item label="经费编号">
        <el-input v-model="formData.funding_number" placeholder="请输入经费编号" />
      </el-form-item>


      <el-form-item label="负责人">
        <el-select
          v-model="formData.leader_id"
          placeholder="请选择负责人"
          clearable
          filterable
        >
          <!-- 这里需要实现负责人的下拉选项 -->
          <el-option
            v-for="leader in leaderOptions"
            :key="leader.id"
            :label="leader.name"
            :value="leader.id"
          />
        </el-select>
      </el-form-item>


      <el-form-item label="项目状态" prop="status">
        <el-select v-model="formData.status" placeholder="请选择状态">
          <el-option
            v-for="item in statusChoices"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>


      <el-form-item label="项目类型">
        <el-select
          v-model="formData.type_id"
          placeholder="请选择项目类型"
          clearable
        >
          <!-- 这里需要实现项目类型的下拉选项 -->
          <el-option
            v-for="type in typeOptions"
            :key="type.id"
            :label="type.name"
            :value="type.id"
          />
        </el-select>
      </el-form-item>


      <el-form-item label="预算(万元)">
        <el-input-number
          v-model="formData.budget"
          :min="0"
          :precision="2"
          :step="0.1"
          controls-position="right"
          style="width: 100%"
        />
      </el-form-item>


      <el-form-item label="承担方式" prop="undertake">
        <el-select v-model="formData.undertake" placeholder="请选择承担方式">
          <el-option
            v-for="item in undertakeChoices"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>


      <el-form-item label="开始日期">
        <el-date-picker
          v-model="formData.start_date"
          type="date"
          placeholder="选择开始日期"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        />
      </el-form-item>


      <el-form-item label="结束日期">
        <el-date-picker
          v-model="formData.end_date"
          type="date"
          placeholder="选择结束日期"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        />
      </el-form-item>


      <el-form-item label="来源单位">
        <el-select
          v-model="formData.source_id"
          placeholder="请选择来源单位"
          clearable
          filterable
        >
          <!-- 这里需要实现来源单位的下拉选项 -->
          <el-option
            v-for="source in sourceOptions"
            :key="source.id"
            :label="source.name"
            :value="source.id"
          />
        </el-select>
      </el-form-item>


      <el-form-item label="研究领域">
        <el-input
          v-model="formData.research_area"
          type="textarea"
          :rows="3"
          placeholder="请输入研究领域"
        />
      </el-form-item>


      <el-form-item label="项目描述">
        <el-input
          v-model="formData.remark"
          type="textarea"
          :rows="3"
          placeholder="请输入项目描述"
        />
      </el-form-item>
    </el-form>


    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submitForm">确定</el-button>
    </template>
  </el-dialog>
</template>


<script setup lang="ts">
import { ref, watch, computed, reactive } from 'vue';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { Project, ProjectForm, Choice } from '@/api/project';
import { projectApi } from '@/api/project';


interface Props {
  modelValue: boolean;
  project?: Project | null;
  statusChoices: Choice[];
  undertakeChoices: Choice[];
}


const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  project: null,
});


const emit = defineEmits(['update:modelValue', 'success']);


const visible = ref(props.modelValue);
const formRef = ref<FormInstance>();
const loading = ref(false);


// 表单数据
const formData = reactive<ProjectForm>({
  title: '',
  number: '',
  funding_number: '',
  leader_id: undefined,
  start_date: '',
  end_date: '',
  status: 'APPROVED',
  type_id: undefined,
  budget: undefined,
  research_area: '',
  source_id: undefined,
  undertake: 'HOST',
  remark: '',
});


// 表单验证规则
const formRules: FormRules = {
  title: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  number: [{ required: true, message: '请输入项目编号', trigger: 'blur' }],
  status: [{ required: true, message: '请选择项目状态', trigger: 'change' }],
  undertake: [{ required: true, message: '请选择承担方式', trigger: 'change' }],
};


// 对话框标题
const formTitle = computed(() => {
  return props.project ? '编辑项目' : '新增项目';
});


// 加载下拉选项数据（这里需要根据实际情况实现）
const leaderOptions = ref<any[]>([]);
const typeOptions = ref<any[]>([]);
const sourceOptions = ref<any[]>([]);


// 监听visible变化
watch(
  () => props.modelValue,
  (val) => {
    visible.value = val;
  }
);


// 监听visible变化并更新父组件
watch(visible, (val) => {
  emit('update:modelValue', val);
  if (val && props.project) {
    // 编辑模式，填充表单数据
    Object.assign(formData, {
      title: props.project.title,
      number: props.project.number,
      funding_number: props.project.funding_number || '',
      leader_id: props.project.leader_id || undefined,
      start_date: props.project.start_date || '',
      end_date: props.project.end_date || '',
      status: props.project.status,
      type_id: props.project.type_id || undefined,
      budget: props.project.budget || undefined,
      research_area: props.project.research_area || '',
      source_id: props.project.source_id || undefined,
      undertake: props.project.undertake,
      remark: props.project.remark || '',
    });
  } else if (val) {
    // 新增模式，重置表单
    if (formRef.value) {
      formRef.value.resetFields();
    }
  }
});


// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;


  try {
    const valid = await formRef.value.validate();
    if (!valid) return;


    loading.value = true;


    if (props.project) {
      // 更新项目
      await projectApi.updateProject(props.project.id, formData);
      ElMessage.success('更新成功');
    } else {
      // 创建项目
      await projectApi.createProject(formData);
      ElMessage.success('创建成功');
    }


    emit('success');
    visible.value = false;
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || '操作失败');
    }
  } finally {
    loading.value = false;
  }
};
</script>
