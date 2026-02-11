import { Link } from 'wouter';
import { BarChart3, TrendingUp } from 'lucide-react';

export default function Navigation() {
  return (
    <nav className="border-b bg-card">
      <div className="container flex items-center justify-between h-16">
        <div className="flex items-center gap-8">
          <Link href="/">
            <a className="flex items-center gap-2 font-bold text-lg hover:text-primary transition-colors">
              <BarChart3 className="h-6 w-6" />
              FMCG Analytics
            </a>
          </Link>
          
          <div className="flex items-center gap-4">
            <Link href="/">
              <a className="text-sm font-medium hover:text-primary transition-colors">
                Dashboard
              </a>
            </Link>
            <Link href="/forecasting">
              <a className="text-sm font-medium hover:text-primary transition-colors flex items-center gap-1">
                <TrendingUp className="h-4 w-4" />
                Forecasting
              </a>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
