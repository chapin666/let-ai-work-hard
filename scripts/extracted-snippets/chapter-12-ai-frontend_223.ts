# Source: chapter-12-ai-frontend.md
# Lines: 223-314
# Language: typescript

// templates/ListPageTemplate.tsx
import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button, Table, Modal, Form, Input, Select, DatePicker, message } from '@/components';
import { useListPage } from '@/hooks/useListPage';
import type { ListPageProps, ColumnConfig } from './types';

/**
 * 通用列表页模板
 * @param api - 数据接口
 * @param columns - 表格列配置
 * @param searchFields - 搜索字段配置
 * @param formFields - 表单字段配置
 * @param title - 页面标题
 */
export function createListPage<T, Q, F>({
  api,
  columns,
  searchFields,
  formFields,
  title,
}: ListPageProps<T, Q, F>) {
  return function ListPage() {
    // 使用封装好的列表页逻辑
    const {
      query,
      setQuery,
      data,
      isLoading,
      modalVisible,
      setModalVisible,
      editingRecord,
      setEditingRecord,
      handleSearch,
      handleReset,
      handleDelete,
      handleSubmit,
    } = useListPage<T, Q, F>({ api });

    return (
      <div className="p-6">
        {/* 页面标题 */}
        <h1 className="text-2xl font-bold mb-6">{title}</h1>
        
        {/* 搜索栏 */}
        <SearchBar
          fields={searchFields}
          onSearch={handleSearch}
          onReset={handleReset}
        />
        
        {/* 操作按钮 */}
        <div className="mb-4 flex gap-2">
          <Button type="primary" onClick={() => setModalVisible(true)}>
            新增
          </Button>
          <Button onClick={handleExport}>导出</Button>
        </div>
        
        {/* 数据表格 */}
        <Table
          columns={columns}
          dataSource={data?.list}
          loading={isLoading}
          pagination={{
            current: query.page,
            pageSize: query.pageSize,
            total: data?.total,
            onChange: (page, pageSize) => setQuery({ ...query, page, pageSize }),
          }}
        />
        
        {/* 表单弹窗 */}
        <Modal
          title={editingRecord ? '编辑' : '新增'}
          open={modalVisible}
          onCancel={() => setModalVisible(false)}
          footer={null}
        >
          <DataForm
            fields={formFields}
            initialValues={editingRecord}
            onSubmit={handleSubmit}
            onCancel={() => setModalVisible(false)}
          />
        </Modal>
      </div>
    );
  };
}
