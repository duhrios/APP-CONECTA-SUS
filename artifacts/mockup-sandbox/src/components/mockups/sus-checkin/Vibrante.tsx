import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, User, HeartPulse, CreditCard, ChevronRight, Activity, MapPinned, Stethoscope } from 'lucide-react';

export function Vibrante() {
  const [step, setStep] = useState(1);
  const totalSteps = 2;

  const nextStep = () => {
    if (step < totalSteps) setStep(step + 1);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 md:p-8 font-sans">
      <div className="w-full max-w-md mx-auto space-y-6">
        {/* Header / Brand */}
        <div className="flex flex-col items-center justify-center space-y-2 mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-[#0AB4A0] to-[#2563EB] flex items-center justify-center shadow-lg">
            <HeartPulse className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-extrabold text-slate-800 tracking-tight">Conecta SUS</h1>
          <p className="text-slate-500 font-medium text-sm">Check-in rápido e humanizado</p>
        </div>

        {/* Form Container */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100 relative">
          {/* Animated Progress Bar */}
          <div className="absolute top-0 left-0 w-full h-1.5 bg-slate-100">
            <div 
              className="h-full bg-gradient-to-r from-[#0AB4A0] to-[#2563EB] transition-all duration-500 ease-out"
              style={{ width: `${(step / totalSteps) * 100}%` }}
            />
          </div>

          <div className="p-6 pt-8">
            {step === 1 ? (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="space-y-1 mb-6">
                  <h2 className="text-xl font-bold text-slate-800">Seus dados</h2>
                  <p className="text-slate-500 text-sm">Preencha para iniciar seu atendimento.</p>
                </div>

                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name" className="text-slate-700 font-semibold flex items-center gap-2">
                      <User className="w-4 h-4 text-[#0AB4A0]" />
                      Nome Completo
                    </Label>
                    <Input 
                      id="name" 
                      placeholder="Maria Silva" 
                      className="rounded-xl border-slate-200 focus:border-[#0AB4A0] focus:ring-[#0AB4A0]/20 h-12"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="cpf" className="text-slate-700 font-semibold flex items-center gap-2">
                      <CreditCard className="w-4 h-4 text-[#0AB4A0]" />
                      CPF ou Cartão do SUS
                    </Label>
                    <Input 
                      id="cpf" 
                      placeholder="000.000.000-00" 
                      className="rounded-xl border-slate-200 focus:border-[#0AB4A0] focus:ring-[#0AB4A0]/20 h-12"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="unit" className="text-slate-700 font-semibold flex items-center gap-2">
                      <Stethoscope className="w-4 h-4 text-[#0AB4A0]" />
                      Unidade de Saúde
                    </Label>
                    <Select>
                      <SelectTrigger className="w-full rounded-xl border-slate-200 focus:border-[#0AB4A0] focus:ring-[#0AB4A0]/20 h-12">
                        <SelectValue placeholder="Selecione a unidade" />
                      </SelectTrigger>
                      <SelectContent className="rounded-xl">
                        <SelectItem value="ubs1">UBS Centro</SelectItem>
                        <SelectItem value="ubs2">UPA Zona Sul</SelectItem>
                        <SelectItem value="ubs3">Clínica da Família</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="pt-2">
                    <Button 
                      variant="outline" 
                      className="w-full rounded-xl h-12 border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900 flex items-center gap-2"
                    >
                      <MapPinned className="w-4 h-4 text-blue-500" />
                      Usar minha localização atual
                    </Button>
                  </div>
                </div>

                <div className="pt-4">
                  <Button 
                    onClick={nextStep}
                    className="w-full h-14 rounded-2xl bg-gradient-to-r from-[#0AB4A0] to-[#2563EB] hover:opacity-90 transition-opacity text-white font-bold text-lg shadow-md shadow-blue-500/25"
                  >
                    Confirmar Check-in
                    <ChevronRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-8 animate-in fade-in zoom-in-95 duration-500 flex flex-col items-center text-center">
                <div className="space-y-2">
                  <h2 className="text-2xl font-bold text-slate-800">Tudo certo, Maria!</h2>
                  <p className="text-slate-500">Seu check-in foi realizado com sucesso.</p>
                </div>

                {/* Queue Number Badge */}
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-tr from-[#0AB4A0] to-[#2563EB] blur-xl opacity-30 rounded-full animate-pulse" />
                  <div className="relative w-48 h-48 bg-white rounded-full border-4 border-[#0AB4A0]/10 flex flex-col items-center justify-center shadow-xl">
                    <span className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">Sua Senha</span>
                    <span className="text-6xl font-black bg-gradient-to-br from-[#0AB4A0] to-[#2563EB] bg-clip-text text-transparent">
                      A42
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 w-full">
                  <div className="bg-slate-50 rounded-2xl p-4 border border-slate-100 flex flex-col items-center">
                    <span className="text-3xl font-bold text-slate-700">3</span>
                    <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide mt-1">Pessoas na frente</span>
                  </div>
                  <div className="bg-blue-50 rounded-2xl p-4 border border-blue-100 flex flex-col items-center">
                    <span className="text-xl font-bold text-blue-700 mt-1">~15 min</span>
                    <span className="text-xs font-semibold text-blue-600/70 uppercase tracking-wide mt-1">Tempo estimado</span>
                  </div>
                </div>

                <div className="bg-emerald-50 rounded-2xl p-4 flex items-start gap-3 w-full border border-emerald-100">
                  <Activity className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                  <p className="text-sm text-emerald-700 text-left font-medium">
                    Aguarde na recepção. Você será chamado em breve pelo painel.
                  </p>
                </div>

                <Button 
                  variant="ghost" 
                  onClick={() => setStep(1)}
                  className="text-slate-500 hover:text-slate-700"
                >
                  Fazer novo check-in
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
