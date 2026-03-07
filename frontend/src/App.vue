<script setup>
import {ref} from 'vue';

const cep = ref('');
let clima = ref(null);

async function buscarclima() {
    let response = await fetch(`http://localhost:8000/cep/${cep.value}`)
    let data = await response.json()
    clima.value = data
    console.log(clima.value)
}

</script>

<template>
  <div>
    <h1>Previsão do Tempo 🌤</h1>

    <input v-model="cep" placeholder="Digite seu CEP" />
    <button @click="buscarclima">Buscar</button>

    <div v-if="clima">
      <p>Cidade: {{ clima.name }}</p>
      <p>Temperatura: {{ clima.main.temp}}°C</p>
      <p>Descrição: {{ clima.weather[0].description }}</p>
      <p>Umidade: {{ clima.main.humidity }}%</p>
    </div>
  </div>
</template>