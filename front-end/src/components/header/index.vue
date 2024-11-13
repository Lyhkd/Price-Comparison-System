<template>
  <!-- Header布局，固定高度 -->
  <n-layout :native-scrollbar="false" has-sider class="layout-header">
    <n-button @click="console.log(searchStore.searchParams)">测试</n-button>
    <!-- 左侧Logo -->
    <n-layout-sider width="60px">
      <div class="logo" @click="$router.push({ name: 'home' })">
        <img src="../../assets/images/logo.png" alt="logo" class="logo-image" />
      </div>
    </n-layout-sider>

    <!-- 中间的导航菜单 -->
    <n-layout-header
      content-style="display: flex; align-items: center; justify-content: space-between; padding: 0 20px;">
      <div class="menu-box">
        <!-- 菜单 -->
        <n-menu :options="menuOptions" mode="horizontal" :default-value="'home'" v-model:value="currentRoute" />
        <!-- 搜索框 -->
        <div class="search-box" v-if="!isSearchHidden">
          <n-input round clearable placeholder="搜索商品..." v-model:value="searchInput" @keydown.enter="onSearch" 
            style="width: 200px;" />
          <div style="width: 5px;"></div>
          <n-button round type="primary" @click="onSearch">
            <template #icon>
              <n-icon>
                <SearchIcon />
              </n-icon>
            </template>
          </n-button>
        </div>
      </div>
    </n-layout-header>


    <!-- 右侧用户头像和设置 -->
    <n-layout-sider width="150">
      <!-- 登陆显示头像 -->
      <div v-if="loginStore.isLogin" style="height: 60px">
        <n-dropdown trigger="hover" @select="avatarSelect" :options="avatarOptions">
          <div class="avatar-box">
            <n-avatar size="medium" round bordered :src="loginStore.loginInfo.avatar">
            </n-avatar>
            <n-divider vertical />
            <span>{{ loginStore.loginInfo.username }}</span>
          </div>

        </n-dropdown>
      </div>
      <!-- 未登录显示注册和登录按钮 -->
      <div class="avatar-box" v-if="!loginStore.isLogin">
        <n-space align="center">
          <n-button text @click="goToAuth('login')">登录</n-button>
          <n-divider vertical />
          <n-button text @click="goToAuth('signup')">注册</n-button>
        </n-space>
      </div>
    </n-layout-sider>
  </n-layout>
</template>

<script lang="ts">
import { defineComponent, h, ref, watch, onMounted, onBeforeUnmount, computed } from "vue";
import { NIcon } from "naive-ui";
import type { MenuOption } from "naive-ui";
import { RouterLink, useRouter, useRoute } from "vue-router";
import { useUserStore } from '@/store/user';
import useLoginStore from "@/store/login";
import useSearchStore from "@/store/search";
import {
  Home as HomeIcon,
  LaptopOutline as WorkIcon,
  PersonSharp as UserIcon,
  PhonePortrait as ItemIcon,
  Search as SearchIcon
} from "@vicons/ionicons5";




export default defineComponent({
  components: {
    NIcon,
    SearchIcon  
  },
  setup(props, { emit }) {
    const router = useRouter();
    const route = useRoute();
    const userStore = useUserStore();
    const loginStore = useLoginStore();
    const searchStore = useSearchStore(); 
    // 用于渲染图标
    function renderIcon(icon: any) {
      return () => h(NIcon, null, { default: () => h(icon) });
    }


    // 搜索处理

    const searchInput = ref<string>('')
    const isSearchHidden = ref<boolean>(false);
    // const onInputChange = (value: string) => {
    //   searchInput.value = value
    // }
    function onSearch() {
      router.push({
        name: 'search',
        query: {
          keyword: searchInput.value,
          order: "default",
          pageNo: 1,
          pageSize: 30,
          platform: "all", // 如果是数组，可以将其转成字符串
        },
        })
      console.log('搜索:', searchInput.value);
    }

    // 计算属性：根据窗口宽度返回是否隐藏搜索框
    const isSearchHiddenComputed = computed(() => {
      return window.innerWidth < 780;
    });
    const handleResize = () => {
      isSearchHidden.value = isSearchHiddenComputed.value;
    };
    onMounted(() => {
      window.addEventListener('resize', handleResize);
      handleResize(); // 初始化检查
    });

    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize);
    });
    // 处理用户下拉菜单点击
    const avatarOptions = [
      {
        label: "个人设置",
        key: 1,
      },
      {
        label: "退出登录",
        key: 2,
      },
    ];

    //头像部分
    const avatarSelect = (key: any) => {
      switch (key) {
        case 1:
          router.push({ name: "Setting" });
          break;
        case 2:
          loginStore.logout();
          router.push({ name: "home" });
          break;
      }
    };


    // 注册和登录按钮
    const onClickRegister = () => {
      router.push({ name: "register" });
    };
    const onClickLogin = () => {
      router.push({ name: "login" });
    };
    const goToAuth = (mode: 'login' | 'signup') => {
      if (currentRoute.value === 'auth') {
        router.push({ path: '/auth', query: { mode } }).then(() => {
          window.location.reload();});
      } else {
        router.push({ path: '/auth', query: { mode } });
      }
      
    }

    // menu部分
    const currentRoute = ref<string | symbol>(route.name || 'home')
    watch(
      () => route.name,
      (newRouteName) => {
        currentRoute.value = newRouteName ?? 'home'
      }
    )
    const menuOptions: MenuOption[] = [
      {
        label: () =>
          h(RouterLink, { to: { name: "home" } }, { default: () => "首页" }),
        key: "home",
        icon: renderIcon(HomeIcon),
      },
      {
        label: () =>
          h(RouterLink, { to: { name: "auth" } }, { default: () => "商品" }),
        key: "item",
        icon: renderIcon(ItemIcon),
      },
      {
        label: () =>
          h(RouterLink, { to: { path: "/user", query: { uid: userStore.userInfo.uid } } }, { default: () => "个人" }),
        key: "user",
        icon: renderIcon(UserIcon),
      },
    ];

    return {
      menuOptions,
      avatarOptions,
      avatarSelect,
      loginStore,
      searchStore,
      searchInput,
      // searchQuery,
      isSearchHidden,
      onSearch,
      // onInputChange,
      onClickRegister,
      onClickLogin,
      goToAuth,
      currentRoute,
    };
  },
});
</script>

<style scoped>
.layout-header {
  height: 60px;
  box-shadow: 0 1px 4px rgba(0, 12, 24, 0.2);

  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    line-height: 60px;
    overflow: hidden;
    white-space: nowrap;
    padding-left: 10px;
    padding-right: 10px;
  }

  .logo-image {
    width: 30px;
    height: 30px;
  }

  .menu-box {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    line-height: 60px;
    overflow: hidden;
    white-space: nowrap;
    padding-left: 10px;
    padding-right: 10px;

    /* 菜单居中 */
    .n-menu {
      flex-grow: 1;
      display: flex;
      justify-content: left;
    }
  }

  /* 用户头像和设置按钮 */
  .user-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .n-layout-header {
    background-color: rgba(241, 241, 241, 0.836);
  }

  .avatar-box {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    width: 150px;
  }

  .search-box {
    display: flex;
    align-items: center;
  }
}

@media (max-width: 800px) {
  .search-box n-input {
    width: 200px !important;
  }
}

/* 在更小的屏幕下，隐藏搜索框 */
@media (max-width: 600px) {
  .search-box {
    display: none;
  }
}

/* Logo样式 */
</style>
