<template>
  <!-- 根组件：路由视图容器 -->
  <!-- 所有页面组件（Home、Cats、Feeding）将在此渲染 -->
  <router-view />
</template>

<style>
/* 全局样式重置与基础配置 */

/* 1. 通用选择器：重置默认样式 + 全局猫爪光标 */
* {
  margin: 0;           /* 移除默认外边距 */
  padding: 0;          /* 移除默认内边距 */
  box-sizing: border-box;  /* 使用border-box盒模型 */
  cursor: url('/noun-paw-1738444.png') 16 16, auto !important;  /* 自定义猫爪光标 */
}

/* 2. HTML 和 Body 基础样式 */
html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;  /* 现代无衬线字体 */
  background: #ffffff;  /* 纯白背景 */
  color: #000000;      /* 纯黑文字 */
  line-height: 1.6;     /* 舒适的行高 */
  cursor: url('/noun-paw-1738444.png') 16 16, auto !important;  /* 确保body也使用猫爪光标 */
}

/* 3. 表单控件样式 */
input, textarea, select, button {
  cursor: url('/noun-paw-1738444.png') 16 16, auto !important;  /* 表单元素也使用猫爪光标 */
}

/* 4. 点击激活状态的光标 */
*:active {
  cursor: url('/noun-paw-1738444 - 副本.png') 16 16, auto !important;  /* 点击时使用另一个光标样式 */
}

/* 5. 滚动条样式 */
::-webkit-scrollbar {
  cursor: url('/noun-paw-1738444.png') 12 12, auto !important;  /* 滚动条区域也使用猫爪光标 */
}
</style>