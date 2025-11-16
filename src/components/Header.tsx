import { Button } from "@/components/ui/button";

const Header = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg overflow-hidden flex items-center justify-center">
            <img src="/logo.png" alt="Iris AI" className="w-full h-full object-contain" />
          </div>
          <span className="text-xl font-bold">Iris AI</span>
        </div>
        {/* login removed to keep project local and authorial */}
      </div>
    </header>
  );
};

export default Header;
