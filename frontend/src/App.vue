<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import Chart from './Chart.vue'
const cep = ref('');
const clima = ref(null);

const particlesKey = ref(0)


const climaAtual = computed(() => {
  // console.log(clima)
  if (!clima.value || !clima.value[0]) return null;
  console.log('teste')


  const hoje = clima.value[0];
  console.log(hoje.horarios[0])

  return hoje.horarios[0];
})

watch(climaAtual, async () => {
  await nextTick()
  particlesKey.value++
})
const options = computed(() => {
  const padrao = {
    background: { color: "#0f172a" },
    particles: {
      number: { value: 50 },
      color: { value: "#ffffff" },
      move: { enable: true, speed: 1 }
    }
  }

  if (!climaAtual.value) return padrao;

  const desc = climaAtual.value.descricao.toLowerCase();

  if (desc.includes('nuvens')) {
    console.log(12)
    if (desc.includes('nuvens')) {
      return JSON.parse(JSON.stringify({
        background: { color: "#1e293b" },
        particles: {
          number: { value: 150 },
          color: { value: "#ffffff" },
          move: {
            enable: true,
            speed: 10,
            direction: "bottom",
            straight: true
          },
          shape: { type: "line" }
        }
      }))
    }
  }

  if (desc.includes('nublado')) {
    return {
      background: { color: "#475569" },
      particles: {
        number: { value: 15 },
        opacity: { value: 0.2 },
        size: { value: 40 },
        move: { enable: true, speed: 0.5 }
      }
    };
  }

  return padrao;
})

async function buscarclima() {
  let response = await fetch(`http://localhost:8000/cep/${cep.value}`)
  clima.value = await response.json()
}

</script>

<template>
  <vue-particles :key="particlesKey" id="tsparticles" :options="options" />

  <div class="conteudo">
    <div class="busca">
      <input v-model="cep" placeholder="Digite seu CEP" @keyup.enter="buscarclima" />
      <button @click="buscarclima">Buscar</button>
    </div>

    <div v-if="climaAtual" class="clima-hoje">
      <h1>Agora em {{ clima[0].name || 'Sua Cidade' }}</h1>
      <p class="temp-principal">{{ climaAtual.temp }}°C</p>
      <p class="status">Status: {{ climaAtual.descricao }}</p>
    </div>

    <div v-if="clima" class="resultados">
      <div v-for="dia in clima.slice(1)" :key="dia.data" class="card-clima">
        <h3>{{ dia.data }}</h3>
        <p class="temp-min-max">
          <span>Min: {{ dia.min }}°C</span> |
          <span>Max: {{ dia.max }}°C</span>
        </p>
        <p class="desc-card">{{ dia.horarios[4]?.descricao || 'Sem dados' }}</p>
      </div>
    </div>
  </div>
</template>

<style>
body,
html {
  margin: 0;
  padding: 0;
  background-color: #0f172a;
}

#tsparticles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

#tsparticles canvas {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
  top: 0 !important;
  left: 0 !important;
  z-index: -1 !important;
  /* Fica atrás do conteúdo */
  pointer-events: none;
}

.conteudo {
  position: relative;
  z-index: 10;
  color: white;
  text-align: center;
  font-family: sans-serif;
  padding-top: 50px;
}

.card-clima {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  display: inline-block;
  margin: 10px;
  padding: 20px;
  border-radius: 8px;
}
</style>