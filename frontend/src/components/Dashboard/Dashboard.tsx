import { useState, useEffect } from 'react';
import { getTransactions, getCategories, getBudgets } from '../../utils/api';
import TransactionForm from './TransactionForm';
import TransactionList from './TransactionList';
import BudgetOverview from './BudgetOverview';
import UsersList from '../Admin/UsersList';

interface Transaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string;
  created_at: string;
}

interface Category {
  id: number;
  name: string;
  description?: string;
  color?: string;
}

interface Budget {
  id: number;
  category_id: number;
  amount: number;
  period: 'monthly' | 'yearly';
}

export default function Dashboard() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [transactionsData, categoriesData, budgetsData] = await Promise.all([
          getTransactions(),
          getCategories(),
          getBudgets()
        ]);
        setTransactions(transactionsData);
        setCategories(categoriesData);
        setBudgets(budgetsData);
        
        // Check if user is admin by trying to fetch users
        try {
          await fetch('http://localhost:8000/users', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          setIsAdmin(true);
        } catch (error) {
          setIsAdmin(false);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleTransactionAdded = (newTransaction: Transaction) => {
    setTransactions([newTransaction, ...transactions]);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left column - Transaction Form */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium mb-4">Add Transaction</h2>
            <TransactionForm
              categories={categories}
              onTransactionAdded={handleTransactionAdded}
            />
          </div>
        </div>

        {/* Middle column - Transaction List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium mb-4">Recent Transactions</h2>
            <TransactionList transactions={transactions} categories={categories} />
          </div>
        </div>

        {/* Right column - Budget Overview */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium mb-4">Budget Overview</h2>
            <BudgetOverview
              budgets={budgets}
              categories={categories}
              transactions={transactions}
            />
          </div>
        </div>
      </div>

      {/* Admin Section */}
      {isAdmin && (
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium mb-4">User Management</h2>
            <UsersList />
          </div>
        </div>
      )}
    </div>
  );
} 