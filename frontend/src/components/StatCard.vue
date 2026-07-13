<template>

<div class="card shadow-sm">
    <div class="card-body">
        <h6 class="text-muted">
            {{ title }}
        </h6>
        <h2>
            {{ value }}
        </h2>
    </div>
</div>

</template>

<script>
export default{
    props:[
        "title",
        "value"
    ]
}
</script>