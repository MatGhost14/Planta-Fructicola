import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Inspeccion from './pages/Inspeccion'
ReactDOM.createRoot(document.getElementById('root')!).render(<BrowserRouter><Routes><Route path='/' element={<Inspeccion/>}/></Routes></BrowserRouter>)