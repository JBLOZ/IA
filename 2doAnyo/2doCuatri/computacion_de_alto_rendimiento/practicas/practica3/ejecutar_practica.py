import practica_cpu_vs_gpu


with open("archivo.md", "w", encoding="utf-8") as f:

    practica = practica_cpu_vs_gpu.PracticaCPUvsGPU(debug=False)
    tabla = practica.run_all()
    f.write(tabla)

    


