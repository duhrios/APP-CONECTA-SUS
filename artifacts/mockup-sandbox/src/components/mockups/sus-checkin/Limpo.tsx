import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { MapPin, User, FileText, CheckCircle2, Clock, MapPinIcon, HeartPulse } from 'lucide-react';

export function Limpo() {
  const [step, setStep] = useState<1 | 2>(1);

  const susBlue = "#0057A8";
  const bgSoft = "#F8FAFC";

  return (
    <div className="min-h-screen font-sans text-slate-800 flex flex-col" style={{ backgroundColor: bgSoft }}>
      {/* Header */}
      <header className="w-full text-white py-4 shadow-sm" style={{ backgroundColor: susBlue }}>
        <div className="max-w-md mx-auto px-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center text-[#0057A8]">
              <HeartPulse size={20} />
            </div>
            <h1 className="text-xl font-semibold tracking-tight">SUS Check-in</h1>
          </div>
          <div className="text-sm font-medium opacity-90">Atendimento Rápido</div>
        </div>
      </header>

      <main className="flex-1 w-full max-w-md mx-auto p-4 flex flex-col gap-6 mt-4">
        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-2">
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${step >= 1 ? 'bg-[#0057A8] text-white' : 'bg-slate-200 text-slate-500'}`}>
              1
            </div>
            <div className={`w-12 h-1 rounded ${step >= 2 ? 'bg-[#0057A8]' : 'bg-slate-200'}`} />
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold ${step >= 2 ? 'bg-[#0057A8] text-white' : 'bg-slate-200 text-slate-500'}`}>
              2
            </div>
          </div>
        </div>
        <div className="flex justify-between px-10 text-xs font-medium text-slate-500 -mt-6">
          <span className={step >= 1 ? "text-[#0057A8]" : ""}>Identificação</span>
          <span className={step >= 2 ? "text-[#0057A8]" : ""}>Aguardar</span>
        </div>

        {step === 1 ? (
          <Card className="border-0 shadow-md">
            <CardHeader className="pb-4">
              <CardTitle className="text-2xl text-[#0057A8]">Nova Ficha</CardTitle>
              <CardDescription>Preencha os dados abaixo para retirar sua senha de atendimento.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-slate-700 font-semibold">Nome Completo</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input id="name" placeholder="Ex: Maria da Silva" className="pl-9 border-slate-300 focus-visible:ring-[#0057A8]" />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="document" className="text-slate-700 font-semibold">CPF ou Cartão do SUS</Label>
                <div className="relative">
                  <FileText className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input id="document" placeholder="000.000.000-00" className="pl-9 border-slate-300 focus-visible:ring-[#0057A8]" />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="unit" className="text-slate-700 font-semibold">Unidade de Saúde</Label>
                <Select>
                  <SelectTrigger className="border-slate-300 focus:ring-[#0057A8]">
                    <SelectValue placeholder="Selecione a unidade" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="upa-centro">UPA 24h - Centro</SelectItem>
                    <SelectItem value="upa-zona-sul">UPA 24h - Zona Sul</SelectItem>
                    <SelectItem value="ubs-vila-nova">UBS Vila Nova</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="pt-2">
                <Button variant="outline" className="w-full border-dashed border-[#0057A8] text-[#0057A8] hover:bg-blue-50 bg-white justify-start gap-2 h-12">
                  <MapPinIcon className="h-5 w-5" />
                  Usar minha localização atual
                </Button>
                <p className="text-xs text-slate-500 mt-2 text-center">Permita o acesso à localização para encontrar a unidade mais próxima.</p>
              </div>
            </CardContent>
            <CardFooter className="pt-2">
              <Button 
                className="w-full text-white h-12 text-lg hover:bg-blue-800" 
                style={{ backgroundColor: susBlue }}
                onClick={() => setStep(2)}
              >
                Gerar Senha
              </Button>
            </CardFooter>
          </Card>
        ) : (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Card className="border-0 shadow-lg text-center overflow-hidden">
              <div className="bg-[#0057A8] text-white py-3 text-sm font-medium">
                Sua senha foi gerada com sucesso
              </div>
              <CardContent className="pt-8 pb-10 space-y-4">
                <div className="text-slate-500 font-medium uppercase tracking-wider text-sm">Senha Normal</div>
                <div className="text-7xl font-bold tracking-tighter text-[#0057A8]">
                  N42
                </div>
                <div className="inline-flex items-center gap-2 bg-blue-50 text-[#0057A8] px-4 py-2 rounded-full font-medium text-sm border border-blue-100">
                  <Clock className="w-4 h-4" />
                  Tempo estimado: 45 min
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm bg-white">
              <CardContent className="p-5 flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-500 font-medium mb-1">Status na Fila</p>
                  <p className="text-lg font-bold text-slate-800">5 pessoas na frente</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center">
                  <User className="text-slate-400 w-6 h-6" />
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm bg-white border-l-4" style={{ borderLeftColor: susBlue }}>
              <CardContent className="p-4 flex gap-3">
                <MapPin className="text-[#0057A8] w-5 h-5 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-slate-800 text-sm">UPA 24h - Centro</p>
                  <p className="text-xs text-slate-500 mt-1">Av. Principal, 1000 - Centro</p>
                  <p className="text-xs text-slate-500">Aguarde ser chamado pelo painel eletrônico.</p>
                </div>
              </CardContent>
            </Card>
            
            <Button variant="ghost" className="w-full text-slate-500 hover:text-slate-800" onClick={() => setStep(1)}>
              Voltar ao início
            </Button>
          </div>
        )}
      </main>
    </div>
  );
}
