#pragma once

struct bContext
{
  int thread;

  struct
  {
    void *manager;
    void *window;
    void *workspace;
    void *screen;
    void *area;
    void *region;
    void *menu;
    void *gizmo_group;
    void *store;

    const char *operator_poll_msg;

    struct PollMsgDyn_Params
    {
      char *(*get_fn)(bContext *, void *);
      char *(*free_fn)(bContext *, void *);
      void *user_data;
    } operator_poll_msg_dyn_params;
  } wm;

  struct
  {
    void *main;
    void *scene;
    int recursion;
    bool py_init;
    void *py_context;
    void *py_context_orig;
  } data;
};
