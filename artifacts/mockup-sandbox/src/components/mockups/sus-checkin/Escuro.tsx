import React, { useState } from 'react';
import { Shield, MapPin, Activity, Fingerprint, CheckCircle2, ChevronRight, User, Hash, Search } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";

export function Escuro() {
  const [step, setStep] = useState<'form' | 'queue'>('form');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setStep('queue');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#0D1B2A] text-slate-200 font-sans flex flex-col md:flex-row selection:bg-[#00C853] selection:text-black overflow-hidden relative">
      {/* Ambient glow effects */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-[#00C853]/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[40%] h-[40%] bg-[#00C853]/5 blur-[100px] rounded-full pointer-events-none" />

      {/* Sidebar */}
      <aside className="w-full md:w-80 bg-[#152438]/80 backdrop-blur-xl border-r border-[#1e3450] p-8 flex flex-col relative z-10">
        <div className="flex items-center gap-3 mb-12">
          <div className="w-10 h-10 rounded-lg bg-[#00C853]/20 flex items-center justify-center border border-[#00C853]/50 shadow-[0_0_15px_rgba(0,200,83,0.3)]">
            <Activity className="text-[#00C853] w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-wider">SUS<span className="text-[#00C853]">DIGITAL</span></h1>
            <p className="text-xs text-slate-400 uppercase tracking-widest">Portal de Acesso</p>
          </div>
        </div>

        <nav className="flex-1 space-y-6">
          <div className="relative">
            {step === 'queue' && (
              <div className="absolute left-[11px] top-8 bottom-[-24px] w-0.5 bg-[#00C853]/30" />
            )}
            <div className="flex items-start gap-4">
              <div className={`w-6 h-6 rounded-full flex items-center justify-center border-2 mt-0.5 shrink-0 transition-colors duration-500 ${step === 'form' ? 'border-[#00C853] bg-[#00C853]/20 shadow-[0_0_10px_rgba(0,200,83,0.5)]' : 'border-[#00C853] bg-[#00C853] text-[#0D1B2A]'}`}>
                {step === 'queue' ? <CheckCircle2 className="w-4 h-4" /> : <span className="text-xs font-bold text-[#00C853]">1</span>}
              </div>
              <div>
                <h3 className={`font-semibold ${step === 'form' ? 'text-white' : 'text-slate-400'}`}>Identificação</h3>
                <p className="text-sm text-slate-500">Dados do paciente</p>
              </div>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center border-2 mt-0.5 shrink-0 transition-colors duration-500 ${step === 'queue' ? 'border-[#00C853] bg-[#00C853]/20 shadow-[0_0_10px_rgba(0,200,83,0.5)]' : 'border-[#1e3450] bg-transparent'}`}>
              <span className={`text-xs font-bold ${step === 'queue' ? 'text-[#00C853]' : 'text-slate-600'}`}>2</span>
            </div>
            <div>
              <h3 className={`font-semibold ${step === 'queue' ? 'text-white' : 'text-slate-500'}`}>Fila de Espera</h3>
              <p className="text-sm text-slate-600">Acompanhamento</p>
            </div>
          </div>
        </nav>

        <div className="mt-auto pt-8 border-t border-[#1e3450]">
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <Shield className="w-4 h-4 text-[#00C853]" />
            <span>Conexão Segura e Criptografada</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col p-6 md:p-12 relative z-10 overflow-y-auto">
        <div className="max-w-2xl w-full mx-auto my-auto">
          {step === 'form' ? (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">Check-in de Paciente</h2>
                <p className="text-slate-400">Insira seus dados para entrar na fila de triagem da unidade.</p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <Card className="bg-[#152438]/50 border-[#1e3450] backdrop-blur-md">
                  <CardContent className="p-6 space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="name" className="text-slate-300 flex items-center gap-2">
                        <User className="w-4 h-4 text-[#00C853]" /> Nome Completo
                      </Label>
                      <Input 
                        id="name" 
                        placeholder="Ex: Maria da Silva" 
                        required
                        className="bg-[#0D1B2A] border-[#1e3450] text-white placeholder:text-slate-600 focus-visible:ring-[#00C853] focus-visible:border-[#00C853] h-12"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="doc" className="text-slate-300 flex items-center gap-2">
                        <Fingerprint className="w-4 h-4 text-[#00C853]" /> CPF ou Cartão do SUS
                      </Label>
                      <Input 
                        id="doc" 
                        placeholder="000.000.000-00" 
                        required
                        className="bg-[#0D1B2A] border-[#1e3450] text-white placeholder:text-slate-600 focus-visible:ring-[#00C853] focus-visible:border-[#00C853] h-12 font-mono"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="unit" className="text-slate-300 flex items-center gap-2">
                        <Search className="w-4 h-4 text-[#00C853]" /> Unidade de Saúde
                      </Label>
                      <Select required defaultValue="ubs-centro">
                        <SelectTrigger id="unit" className="bg-[#0D1B2A] border-[#1e3450] text-white focus:ring-[#00C853] h-12">
                          <SelectValue placeholder="Selecione a unidade" />
                        </SelectTrigger>
                        <SelectContent className="bg-[#152438] border-[#1e3450] text-white">
                          <SelectItem value="ubs-centro" className="focus:bg-[#0D1B2A] focus:text-[#00C853]">UBS Centro - Dr. Arnaldo</SelectItem>
                          <SelectItem value="upa-norte" className="focus:bg-[#0D1B2A] focus:text-[#00C853]">UPA Zona Norte</SelectItem>
                          <SelectItem value="hosp-municipal" className="focus:bg-[#0D1B2A] focus:text-[#00C853]">Hospital Municipal</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="pt-2">
                      <Button 
                        type="button" 
                        variant="outline" 
                        className="w-full h-12 bg-transparent border-[#1e3450] text-slate-300 hover:bg-[#1e3450] hover:text-white flex items-center gap-2"
                      >
                        <MapPin className="w-4 h-4 text-[#00C853]" />
                        Usar minha localização para encontrar a unidade mais próxima
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full h-14 bg-[#00C853] hover:bg-[#00E676] text-[#0D1B2A] font-bold text-lg rounded-lg shadow-[0_0_20px_rgba(0,200,83,0.4)] hover:shadow-[0_0_30px_rgba(0,200,83,0.6)] transition-all duration-300"
                >
                  {loading ? (
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 border-2 border-[#0D1B2A] border-t-transparent rounded-full animate-spin" />
                      Processando...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center gap-2">
                      Confirmar Check-in <ChevronRight className="w-5 h-5" />
                    </div>
                  )}
                </Button>
              </form>
            </div>
          ) : (
            <div className="space-y-10 animate-in fade-in zoom-in-95 duration-700 flex flex-col items-center text-center">
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">Check-in Realizado</h2>
                <p className="text-slate-400">Aguarde ser chamado no painel da unidade.</p>
              </div>

              <div className="relative">
                {/* Outer pulsing rings */}
                <div className="absolute inset-0 rounded-full border border-[#00C853]/30 animate-[ping_3s_ease-in-out_infinite]" />
                <div className="absolute inset-[-20px] rounded-full border border-[#00C853]/10 animate-[ping_3s_ease-in-out_infinite_500ms]" />
                
                <div className="w-64 h-64 rounded-full bg-[#152438] border-2 border-[#00C853] shadow-[0_0_50px_rgba(0,200,83,0.2)] flex flex-col items-center justify-center relative z-10">
                  <span className="text-[#00C853] text-lg font-mono font-bold tracking-widest uppercase mb-2">Sua Senha</span>
                  <span className="text-7xl font-bold text-white tracking-tighter drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">
                    N-42
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 w-full max-w-md">
                <Card className="bg-[#152438]/50 border-[#1e3450] backdrop-blur-md">
                  <CardContent className="p-4 flex flex-col items-center justify-center text-center">
                    <span className="text-slate-400 text-sm mb-1">Posição na fila</span>
                    <span className="text-2xl font-bold text-white">5º</span>
                  </CardContent>
                </Card>
                <Card className="bg-[#152438]/50 border-[#1e3450] backdrop-blur-md">
                  <CardContent className="p-4 flex flex-col items-center justify-center text-center">
                    <span className="text-slate-400 text-sm mb-1">Tempo estimado</span>
                    <span className="text-2xl font-bold text-white">~15 min</span>
                  </CardContent>
                </Card>
              </div>

              <div className="w-full max-w-md p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30 flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center shrink-0">
                  <Activity className="w-4 h-4 text-yellow-500" />
                </div>
                <div className="text-left">
                  <h4 className="text-yellow-500 font-semibold text-sm">Status da Triagem</h4>
                  <p className="text-slate-300 text-sm mt-1">Dirija-se à sala de triagem 02 assim que seu número aparecer no painel principal.</p>
                </div>
              </div>

              <Button 
                onClick={() => setStep('form')}
                variant="ghost" 
                className="text-slate-400 hover:text-white hover:bg-[#1e3450]"
              >
                Voltar ao início
              </Button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
