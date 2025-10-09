-- CreateTable
CREATE TABLE "Inspeccion" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "inspector" TEXT NOT NULL,
    "contenedor" TEXT NOT NULL,
    "fecha" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "observaciones" TEXT,
    "temperatura" TEXT NOT NULL,
    "sello" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Evidencia" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "inspeccionId" TEXT NOT NULL,
    "hash" TEXT NOT NULL,
    "rutaArchivo" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Evidencia_inspeccionId_fkey" FOREIGN KEY ("inspeccionId") REFERENCES "Inspeccion" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
