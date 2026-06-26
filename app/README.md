# DolphiSIC Redesign

Variante isolée de DolphiSIC avec barre de navigation horizontale 21st.dev.

## Structure

- Composants shadcn : `components/ui`
- Styles Tailwind : `app/globals.css`
- Composant demandé : `components/ui/navbar.tsx`
- Copie fonctionnelle existante : `public/legacy`
- Backend et bases copiés : `backend`

Le chemin `components/ui` est conservé car il correspond à l'alias shadcn `@/components/ui` et permet au CLI d'ajouter ou mettre à jour des composants sans imports personnalisés.

## Installation manuelle

```bash
npm install
npm run dev
```

Dans un projet vide, la structure équivalente peut être initialisée avec :

```bash
npx shadcn@latest init
npm install framer-motion
```

TypeScript, Tailwind et la configuration shadcn sont déjà présents dans cette copie.

## Lancement complet

Double-cliquer sur `start-redesign.bat`. Backend : `5001`. Frontend : `3000`.
