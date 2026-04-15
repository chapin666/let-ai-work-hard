# Source: chapter-14-ai-refactoring.md
# Lines: 190-283
# Language: javascript

// src/modules/order/list.js
// 原app.js中订单列表相关代码提取

import { formatDate, formatMoney } from '../../utils/format';
import { showToast, showConfirm } from '../../components/dialog';

/**
 * 订单列表模块
 */
export class OrderList {
  constructor(container) {
    this.container = container;
    this.currentPage = 1;
    this.pageSize = 20;
    this.filters = {};
  }

  /**
   * 初始化列表
   */
  init() {
    this.bindEvents();
    this.loadData();
  }

  /**
   * 绑定事件
   */
  bindEvents() {
    // 搜索按钮
    this.container.on('click', '.js-search', () => {
      this.handleSearch();
    });

    // 分页按钮
    this.container.on('click', '.js-page', (e) => {
      const page = $(e.currentTarget).data('page');
      this.goToPage(page);
    });

    // ... 其他事件绑定
  }

  /**
   * 加载数据
   */
  async loadData() {
    try {
      showLoading();
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          page: this.currentPage,
          pageSize: this.pageSize,
          ...this.filters,
        }),
      });

      const data = await response.json();
      this.render(data);
    } catch (error) {
      showToast('加载失败：' + error.message);
    } finally {
      hideLoading();
    }
  }

  /**
   * 渲染列表
   */
  render(data) {
    const html = data.list.map(order => `
      <tr data-id="${order.id}">
        <td>${order.orderNo}</td>
        <td>${order.customerName}</td>
        <td>${formatMoney(order.amount)}</td>
        <td>${this.renderStatus(order.status)}</td>
        <td>${formatDate(order.createdAt)}</td>
        <td>
          <button class="btn-view" data-id="${order.id}">查看</button>
          <button class="btn-edit" data-id="${order.id}">编辑</button>
        </td>
      </tr>
    `).join('');

    this.container.find('.order-table tbody').html(html);
    this.renderPagination(data.total);
  }

  // ... 其他方法
}
