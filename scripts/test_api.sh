#!/bin/bash
# Script para testar as APIs de Permissions e Categories

BASE_URL="http://localhost:8000/api/v1"
AUTH_URL="http://localhost:8000/api/auth"

echo "==========================================="
echo "  MOA Backend API - Testes de Integração"
echo "==========================================="
echo ""

# Função para fazer requisições
request() {
    local method=$1
    local endpoint=$2
    local data=$3

    echo "----------------------------------------"
    echo "📡 $method $endpoint"
    echo "----------------------------------------"

    if [ -n "$data" ]; then
        curl -s -X "$method" "${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data" | python3 -m json.tool 2>/dev/null || echo "Failed to parse JSON"
    else
        curl -s -X "$method" "${endpoint}" \
            -H "Content-Type: application/json" | python3 -m json.tool 2>/dev/null || echo "Failed to parse JSON"
    fi
    echo ""
}

# Test 1: Health Check
echo "🔍 TEST 1: Health Check"
request GET "http://localhost:8000/health"

# Test 2: Root endpoint
echo "🔍 TEST 2: Root Endpoint"
request GET "http://localhost:8000/"

# Test 3: List Categories
echo "🔍 TEST 3: List Categories"
request GET "${BASE_URL}/categories/"

# Test 4: Create Category
echo "🔍 TEST 4: Create Category"
request POST "${BASE_URL}/categories/" '{"name": "Teste Category", "description": "Categoria de teste criada via script"}'

# Test 5: Get Category by Name
echo "🔍 TEST 5: Get Category by Name"
request GET "${BASE_URL}/categories/search/by-name?name=Eletrônicos"

# Test 6: List Permissions
echo "🔍 TEST 6: List Permissions"
request GET "${AUTH_URL}/permissions"

# Test 7: Create Permission
echo "🔍 TEST 7: Create Permission"
request POST "${AUTH_URL}/permissions" '{"nome": "test.permission", "descricao": "Permissão de teste criada via script"}'

# Test 8: Get Permission by Name
echo "🔍 TEST 8: Get Permission by Name"
request GET "${AUTH_URL}/permissions/by-name/permissions.read"

echo "==========================================="
echo "  Testes Concluídos!"
echo "==========================================="

