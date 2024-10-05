import subprocess
import os
import re

class IntelCodeOptimizer:
    def __init__(self, code_filename):
        self.code_filename = code_filename
        self.optimization_suggestions = []
    
    def _load_code(self):
        """Load the C++ code from file."""
        try:
            with open(self.code_filename, 'r') as file:
                code = file.read()
            return code
        except FileNotFoundError:
            print(f"File {self.code_filename} not found.")
            return None

    def analyze_code_structure(self, code):
        """Perform basic analysis of the code structure for optimizations."""
        # Check for loops that could be parallelized (simple pattern matching)
        loop_patterns = re.findall(r"for\s*\(.*\)", code)
        for loop in loop_patterns:
            if "int" in loop and "<" in loop:
                self.optimization_suggestions.append("Consider parallelizing the loop using DPC++ or OpenMP.")
        print("Analysis complete.")
    
    def suggest_vectorization(self):
        """Suggest vectorization techniques."""
        # Suggest vectorization for loops
        self.optimization_suggestions.append("Try using SIMD vectorization for eligible loops using Intel's Vectorization Advisor.")

    def suggest_memory_optimizations(self):
        """Suggest memory optimizations."""
        self.optimization_suggestions.append("Consider optimizing memory access patterns to improve cache usage.")

    def run_vtune_analysis(self):
        """Run Intel VTune Profiler for deeper analysis."""
        print("Running Intel VTune Profiler for analysis...")
        try:
            result = subprocess.run(["vtune", "-collect", "hotspots", self.code_filename], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("VTune Profiler error:", result.stderr)
        except FileNotFoundError:
            print("VTune Profiler not found. Ensure it is installed and set up in your environment.")

    def optimize_with_dpcpp(self):
        """Invoke the DPC++ compiler with optimizations."""
        print("Compiling with Intel DPC++ for further optimizations...")
        try:
            result = subprocess.run(["icpx", "-fsycl", self.code_filename, "-o", "optimized_output.exe"], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Compilation error:", result.stderr)
        except FileNotFoundError:
            print("DPC++ compiler not found. Ensure Intel oneAPI is properly installed.")
    
    def optimize_code(self):
        """Perform code analysis and suggest optimizations."""
        code = self._load_code()
        if code:
            print("Analyzing code...")
            self.analyze_code_structure(code)
            self.suggest_vectorization()
            self.suggest_memory_optimizations()
            print("\nOptimization suggestions:")
            for suggestion in self.optimization_suggestions:
                print(f" - {suggestion}")
    
    def execute(self):
        """Execute the full optimization workflow."""
        self.optimize_code()
        run_profiler = input("Run Intel VTune Profiler for deeper analysis? (y/n) ")
        if run_profiler.lower() == 'y':
            self.run_vtune_analysis()
        run_dpcpp = input("Compile with DPC++ for optimizations? (y/n) ")
        if run_dpcpp.lower() == 'y':
            self.optimize_with_dpcpp()


# Example usage
if __name__ == "__main__":
    optimizer = IntelCodeOptimizer("example_code.cpp")
    optimizer.execute()