# Source: chapter-04-prompt-engineering-basics.md
# Lines: 130-221
# Language: typescript

// AI生成的代码（节选）
import { Response } from 'express';
import { PrismaClient } from '@prisma/client';
import * as XLSX from 'xlsx';
import { createObjectCsvStringifier } from 'csv-writer';
import WebSocket from 'ws';

const prisma = new PrismaClient();

interface ExportParams {
  format: 'csv' | 'xlsx';
  table: string;
  filters?: Record<string, any>;
}

export async function exportData(
  params: ExportParams, 
  ws: WebSocket,
  res: Response
) {
  const startTime = Date.now();
  const filename = `${params.table}_${formatDate(new Date())}.${params.format}`;
  
  try {
    // 获取总记录数
    const totalCount = await prisma[params.table].count({
      where: params.filters
    });
    
    ws.send(JSON.stringify({
      type: 'start',
      total: totalCount,
      message: `开始导出${totalCount}条记录`
    }));

    // 流式处理，每次1000条
    const batchSize = 1000;
    let processedCount = 0;
    const chunks: any[] = [];

    for (let skip = 0; skip < totalCount; skip += batchSize) {
      const records = await prisma[params.table].findMany({
        where: params.filters,
        skip,
        take: batchSize
      });

      chunks.push(...records);
      processedCount += records.length;

      // 发送进度
      ws.send(JSON.stringify({
        type: 'progress',
        processed: processedCount,
        total: totalCount,
        percentage: Math.round((processedCount / totalCount) * 100)
      }));
    }

    // 根据格式生成文件
    if (params.format === 'csv') {
      await generateCSV(chunks, filename, res);
    } else {
      await generateExcel(chunks, filename, res);
    }

    ws.send(JSON.stringify({
      type: 'complete',
      filename,
      duration: Date.now() - startTime
    }));

  } catch (error) {
    ws.send(JSON.stringify({
      type: 'error',
      message: error.message
    }));
    res.status(500).json({ error: 'Export failed' });
  }
}

// 生成CSV（流式写入）
async function generateCSV(data: any[], filename: string, res: Response) {
  // ... 实现细节
}

// 生成Excel（分sheet处理大文件）
async function generateExcel(data: any[], filename: string, res: Response) {
  // ... 实现细节
}
