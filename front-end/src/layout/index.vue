<script>
/**
 * 操作 layout
 * 负责相应事件的统一分发处理
 */
import { defineComponent } from 'vue';
import Menu from './components/header/index.vue';


export default defineComponent({
    name: 'MainLayout',
    components: {
        Menu,
    },
    props: {},
    setup() {
        return {
        };
    },
});
</script>

<template>
    <div>
        <Menu />
    </div>
</template>

<style scoped lang="scss">
.main-layout {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    font-size: 16px;
    display: flex;
    flex-direction: row;
    position: relative;
    z-index: 9;
    &.full-screen {
        > .left,
        > .centre {
            width: 0;
            opacity: 0;
            pointer-events: none;
        }
    }
    > .left {
        height: 100%;
        background-color: var(--bg-color);
        transition: width 0.2s, opacity 0.2s;
        width: 70px;
    }
    > .centre {
        height: 100%;
        width: var(--menu-width);
        background-color: var(--bg-color-2);
        display: flex;
        flex-direction: column;
        transition: width 0.2s, opacity 0.2s;
        > .logo {
            height: var(--navbar-height);
            padding: 0 10px;
            box-sizing: border-box;
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;
            // color:#444954;
            color: #f0f0f0;
            transition: all 0.2s;
            overflow: hidden;
            box-shadow: var(--box-shadow-2);
            border-bottom: 1px solid rgba(0, 0, 0, 0.47);
            cursor: pointer;
            &.hidden {
                width: 0;
                padding: 0;
                // display: none;
                pointer-events: none;
                > .name {
                    font-size: 0;
                }
            }
            > .img {
                // flex:1 1 0;
                width: 45px;
                height: 45px;
                border-radius: 5px;
                margin-right: 10px;
            }
            > .name {
                width: max-content;
                font-size: 22px;
                font-weight: bold;
                transition: all 0.2s;
            }
        }
        > .main-centre-content {
            height: 0;
            flex: 1 1 0;
            .main-centre-content-container {
                > .search-container {
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                    padding: 10px 10px;
                    box-sizing: border-box;
                }
            }
        }
    }
    > .right {
        height: 100%;
        background-color: var(--bg-color-3);
        background-image: linear-gradient(to right, var(--bg-color-3) 0%, var(--bg-color-2) 100%);
        flex: 1 1 0;
        width: 0;
        display: flex;
        flex-direction: column;
        position: relative;
        z-index: 8;
        overflow: hidden;
        > .top {
            height: var(--navbar-height);
            width: 100%;
            // border-bottom: 1px solid rgb(218, 218, 218);
            box-sizing: border-box;
            box-shadow: 0 0 5px #242425;
            position: relative;
            z-index: 2;
            box-shadow: var(--box-shadow-2);
            border-bottom: 1px solid rgba(0, 0, 0, 0.47);
        }
        > .view-container {
            flex: 1 1 0;
            height: 0;
            width: 100%;
            overflow: hidden;
            position: relative;
            z-index: 1;
            > .iframe-view {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
                > iframe {
                    position: absolute;
                    top: 0;
                    left: 0;
                    z-index: -1;
                }
            }
            > .option-bt-list {
                position: absolute;
                top: 5px;
                left: 0;
                width: 100%;
                opacity: 0;
                pointer-events: none;
                display: flex;
                justify-content: center;
                align-items: center;
                transition: all 0.2s;
                z-index: 999;
                &.show {
                    opacity: 1;
                    pointer-events: initial;
                }
                > .container {
                    width: auto;
                    border-radius: 3px;
                    background-color: rgb(255, 255, 255);
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    padding: 5px;
                    box-sizing: border-box;
                    box-shadow: rgba(0, 0, 0, 0.476) 0px 1px 3px;
                    > * {
                        margin-right: 5px;
                        cursor: pointer;
                        border-radius: 3px;
                        box-shadow: inset 0 1px 4px #0000001f;
                        padding: 7px;
                        color: #444954;
                        &:last-child {
                            margin: 0;
                        }
                    }
                }
            }
        }
    }
    > .head-container {
        width: 100%;
        height: var(--navbar-height);
        // border-bottom: 1px solid rgb(218, 218, 218);
        box-sizing: border-box;
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: row;
        box-shadow: var(--box-shadow-2);
        > .left {
            width: var(--menu-width);
            height: 100%;
            padding: 0 10px;
            box-sizing: border-box;
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;
            background-color: var(--bg-color-2);
            // color:#444954;
            color: #f0f0f0;
            transition: all 0.2s;
            overflow: hidden;
            &.hidden {
                width: 0;
                padding: 0;
                // display: none;
                pointer-events: none;
                > .name {
                    font-size: 0;
                }
            }
            > .logo {
                // flex:1 1 0;
                width: 45px;
                height: 45px;
                border-radius: 5px;
                cursor: pointer;
                margin-right: 10px;
            }
            > .name {
                width: max-content;
                font-size: 22px;
                font-weight: bold;
                transition: all 0.2s;
            }
        }
        > .right {
            flex: 1 1 0;
            width: 0;
            height: 100%;
            box-sizing: border-box;
            background-color: var(--bg-color-3);
        }
    }
    > .content-container {
        flex: 1 1 0;
        height: 0;
        width: 100%;
        display: flex;
        flex-direction: row;
        position: relative;
        z-index: 8;
        > .left {
            width: var(--menu-width);
            height: 100%;
            overflow-y: auto;
            // border-right: 1px solid rgb(218, 218, 218);
            box-sizing: border-box;
            position: relative;
            z-index: 9;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.177);
            background-color: var(--bg-color-2);
            transition: width 0.2s;
            overflow: hidden;
            &.hidden {
                width: 0;
                // display: none;
                pointer-events: none;
            }
        }
        > .right {
            flex: 1 1 0;
            width: 0;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 8;
            overflow: hidden;
            background-color: var(--bg-color-3);
            > .top {
                height: var(--tags-height);
                width: 100%;
                // border-bottom: 1px solid rgb(218, 218, 218);
                box-sizing: border-box;
                box-shadow: 0 0 5px #242425;
                position: relative;
                z-index: 2;
            }
            > .view-container {
                flex: 1 1 0;
                height: 0;
                width: 100%;
                overflow: hidden;
                position: relative;
                z-index: 1;
                > .iframe-view {
                    width: 100%;
                    height: 100%;
                    position: absolute;
                    top: 0;
                    left: 0;
                    z-index: 1;
                    > iframe {
                        position: absolute;
                        top: 0;
                        left: 0;
                        z-index: -1;
                    }
                }
                > .option-bt-list {
                    position: absolute;
                    top: 5px;
                    left: 0;
                    width: 100%;
                    opacity: 0;
                    pointer-events: none;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    transition: all 0.2s;
                    z-index: 999;
                    &.show {
                        opacity: 1;
                        pointer-events: initial;
                    }
                    > .container {
                        width: auto;
                        border-radius: 3px;
                        background-color: rgb(255, 255, 255);
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        padding: 5px;
                        box-sizing: border-box;
                        box-shadow: rgba(0, 0, 0, 0.476) 0px 1px 3px;
                        > * {
                            margin-right: 5px;
                            cursor: pointer;
                            border-radius: 3px;
                            box-shadow: inset 0 1px 4px #0000001f;
                            padding: 7px;
                            color: #444954;
                            &:last-child {
                                margin: 0;
                            }
                        }
                    }
                }
            }
        }
    }
}
</style>
