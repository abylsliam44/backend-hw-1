interface Category {
  id: number;
  name: string;
}

interface Transaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string;
  created_at: string;
}

interface TransactionListProps {
  transactions: Transaction[];
  categories: Category[];
}

export default function TransactionList({ transactions, categories }: TransactionListProps) {
  const getCategoryName = (categoryId: number) => {
    const category = categories.find((c) => c.id === categoryId);
    return category?.name || 'Unknown';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="space-y-4">
      {transactions.length === 0 ? (
        <p className="text-gray-500 text-center">No transactions yet</p>
      ) : (
        <div className="space-y-4">
          {transactions.map((transaction) => (
            <div
              key={transaction.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <p className="font-medium">
                  {getCategoryName(transaction.category_id)}
                </p>
                <p className="text-sm text-gray-500">
                  {transaction.description || 'No description'}
                </p>
                <p className="text-xs text-gray-400">
                  {formatDate(transaction.created_at)}
                </p>
              </div>
              <div
                className={`font-medium ${
                  transaction.type === 'income'
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {transaction.type === 'income' ? '+' : '-'}$
                {transaction.amount.toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
} 