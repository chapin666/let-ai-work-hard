# Source: chapter-07-ai-ide-advanced.md
# Lines: 100-150
# Language: typescript

// stores/chartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ChartData, UserConfig } from '@/types';

interface ChartState {
  // 状态
  data: ChartData[];
  config: UserConfig;
  loading: boolean;
  error: string | null;
  
  // Actions
  setData: (data: ChartData[]) => void;
  updateConfig: (config: Partial<UserConfig>) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  data: [],
  config: {
    theme: 'light',
    autoRefresh: false,
    refreshInterval: 60,
  },
  loading: false,
  error: null,
};

export const useChartStore = create<ChartState>()(
  persist(
    (set) => ({
      ...initialState,
      setData: (data) => set({ data }),
      updateConfig: (config) => set((state) => ({
        config: { ...state.config, ...config },
      })),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
      reset: () => set(initialState),
    }),
    {
      name: 'chart-storage',
      partialize: (state) => ({ config: state.config }),
    }
  )
);
