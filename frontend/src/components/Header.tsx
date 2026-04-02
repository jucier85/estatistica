import { Shield } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-900 to-blue-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-3">
        <Shield className="w-8 h-8" />
        <div>
          <h1 className="text-xl font-bold tracking-tight">Estatística Policial</h1>
          <p className="text-blue-200 text-sm">Dashboard de Produtividade com IA</p>
        </div>
      </div>
    </header>
  )
}
