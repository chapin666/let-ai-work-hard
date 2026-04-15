# Source: chapter-12-ai-frontend.md
# Lines: 318-344
# Language: typescript

// pages/OrderList/index.tsx
import { createListPage } from '@/templates/ListPageTemplate';
import { orderApi } from '@/api/order';

export default createListPage({
  title: '订单管理',
  api: orderApi,
  columns: [
    { title: '订单号', dataIndex: 'orderNo', width: 200 },
    { title: '客户', dataIndex: 'customerName' },
    { title: '金额', dataIndex: 'amount', render: (v) => `¥${v.toFixed(2)}` },
    { title: '状态', dataIndex: 'status', enum: orderStatusMap },
    { title: '创建时间', dataIndex: 'createdAt', type: 'datetime' },
  ],
  searchFields: [
    { name: 'orderNo', label: '订单号', type: 'input' },
    { name: 'status', label: '状态', type: 'select', options: orderStatusOptions },
    { name: 'dateRange', label: '日期', type: 'dateRange' },
  ],
  formFields: [
    { name: 'customerName', label: '客户', required: true },
    { name: 'amount', label: '金额', type: 'number', required: true },
    { name: 'status', label: '状态', type: 'select', required: true },
  ],
});
