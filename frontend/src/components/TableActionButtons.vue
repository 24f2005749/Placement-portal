<template>
    <div>
        <button class="btn btn-sm btn-primary me-2" @click="$emit('view')">
            View
        </button>
        <button class="btn btn-sm btn-warning me-2" @click="$emit('edit')">
            Edit
        </button>
        <button class="btn btn-sm btn-danger" @click="$emit('delete')">
            Delete
        </button>
    </div>
</template>

<script>
export default {}
</script>