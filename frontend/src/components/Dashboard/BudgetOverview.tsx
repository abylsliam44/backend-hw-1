interface Category {
  id: number;
  name: string;
  description?: string;
  color?: string;
}

interface Transaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string;
  created_at: string;
}

interface Budget {
  id: number;
  category_id: number;
  amount: number;
  month: number;
  year: number;
}

interface BudgetOverviewProps {
  budgets: Budget[];
  categories: Category[];
  transactions: Transaction[];
}

export default function BudgetOverview({
  budgets,
  categories,
  transactions,
}: BudgetOverviewProps) {
  const getCategoryName = (categoryId: number) => {
    const category = categories.find((c) => c.id === categoryId);
    return category?.name || 'Unknown';
  };

  const calculateSpentAmount = (categoryId: number) => {
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);

    return transactions
      .filter(
        (t) =>
          t.category_id === categoryId &&
          t.type === 'expense' &&
          new Date(t.created_at) >= startOfMonth
      )
      .reduce((sum, t) => sum + t.amount, 0);
  };

  return (
    <div className="space-y-4">
      {budgets.length === 0 ? (
        <p className="text-gray-500 text-center">No budgets set</p>
      ) : (
        <div className="space-y-4">
          {budgets.map((budget) => {
            const spentAmount = calculateSpentAmount(budget.category_id);
            const percentage = (spentAmount / budget.amount) * 100;

            return (
              <div key={budget.id} className="space-y-2">
                <div className="flex justify-between items-center">
                  <p className="font-medium">
                    {getCategoryName(budget.category_id)}
                  </p>
                  <p className="text-sm text-gray-500">
                    ${spentAmount.toFixed(2)} / ${budget.amount.toFixed(2)}
                  </p>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      percentage > 100
                        ? 'bg-red-500'
                        : percentage > 80
                        ? 'bg-yellow-500'
                        : 'bg-green-500'
                    }`}
                    style={{ width: `${Math.min(percentage, 100)}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
} 